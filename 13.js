// =====================================================
// Obsidian "Learn Topic" Script
// Creates a summary note for any topic in your vault
// =====================================================

// ---- Configuration ----
const OUTPUT_FOLDER = "";           // leave empty for root, or "Folder/Subfolder"
const SNIPPET_LENGTH = 80;          // characters before/after the match
const WHOLE_WORD = false;           // true = match whole words only
// -----------------------

// ---- Helper: get user input ----
async function getTopic() {
  const { default: notice } = app.plugins.plugins["templater"].modules.notices;
  return await notice.prompt("Enter topic to learn about:");
}

// ---- Main function ----
async function learnTopic() {
  const topic = await getTopic();
  if (!topic) return;

  const files = app.vault.getMarkdownFiles();
  const results = [];

  // Build regex (case-insensitive)
  const regex = WHOLE_WORD
    ? new RegExp(`\\b${topic.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, "gi")
    : new RegExp(topic.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "gi");

  // Scan every file
  for (const file of files) {
    const content = await app.vault.read(file);
    let match;
    const matches = [];
    // Reset regex lastIndex
    regex.lastIndex = 0;
    while ((match = regex.exec(content)) !== null) {
      const start = Math.max(0, match.index - SNIPPET_LENGTH);
      const end = Math.min(content.length, match.index + match[0].length + SNIPPET_LENGTH);
      const snippet = content.substring(start, end)
        .replace(/\n/g, " ")
        .replace(/\s+/g, " ")
        .trim();
      matches.push({ snippet, match: match[0] });
    }
    if (matches.length > 0) {
      results.push({
        file: file,
        path: file.path,
        matches: matches,
        matchCount: matches.length,
      });
    }
  }

  // ---- Build the output note ----
  let output = `# Topic: ${topic}\n\n`;
  output += `**Found in ${results.length} file(s).**\n\n`;

  if (results.length === 0) {
    output += `No notes mention "${topic}".\n`;
  } else {
    // Table of contents (optional)
    output += `## 📑 Files that mention "${topic}"\n\n`;
    output += `| File | Context |\n|------|--------|\n`;
    for (const res of results) {
      const link = `[[${res.file.basename}]]`;
      // Show first snippet (or combine multiple)
      const firstSnippet = res.matches[0].snippet;
      output += `| ${link} | ${firstSnippet} |\n`;
    }
    output += `\n`;

    // Detailed sections per file
    output += `## 🔍 Detailed excerpts\n\n`;
    for (const res of results) {
      output += `### [[${res.file.basename}]]\n`;
      for (const m of res.matches) {
        output += `- …${m.snippet}…\n`;
      }
      output += `\n`;
    }

    // Optional: list of backlinks (if the topic note exists, it will show them)
    output += `## 🔗 Backlinks\n\n`;
    output += `> *This section shows notes that link to this topic note.*\n`;
    output += `> (Enable the "Backlinks in document" core plugin to see them live.)\n\n`;
  }

  // ---- Create the note ----
  const fileName = `Topic – ${topic}.md`;
  const folder = OUTPUT_FOLDER ? `${OUTPUT_FOLDER}/` : "";
  const filePath = `${folder}${fileName}`;

  // Ensure folder exists
  if (OUTPUT_FOLDER) {
    const folderExists = app.vault.getAbstractFileByPath(OUTPUT_FOLDER);
    if (!folderExists) {
      await app.vault.createFolder(OUTPUT_FOLDER);
    }
  }

  // Check if file already exists
  const existing = app.vault.getAbstractFileByPath(filePath);
  if (existing) {
    const confirm = await app.plugins.plugins["templater"].modules.notices
      .notice.confirm(`File "${fileName}" already exists. Overwrite?`);
    if (!confirm) return;
    await app.vault.modify(existing, output);
  } else {
    await app.vault.create(filePath, output);
  }

  // Open the new note
  const newFile = app.vault.getAbstractFileByPath(filePath);
  await app.workspace.getLeaf().openFile(newFile);

  new Notice(`✅ Learned "${topic}" – created ${results.length} references.`);
}

// ---- Run ----
module.exports = learnTopic;