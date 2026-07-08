def progress_bar(total=100, prefix="Progress", length=30):
    """Display a dynamic progress bar."""
    for i in range(total + 1):
        percent = i / total
        filled = int(length * percent)
        bar = "█" * filled + "░" * (length - filled)
        sys.stdout.write(f"\r{prefix}: |{bar}| {percent:.1%}")
        sys.stdout.flush()
        time.sleep(0.05)
    print()  # newline after complete

progress_bar(total=50)