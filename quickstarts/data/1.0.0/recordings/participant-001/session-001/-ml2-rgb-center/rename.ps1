Get-ChildItem -Filter '*.png' | ForEach-Object {
    $name = $_.BaseName
    $ext = $_.Extension

    # Find last hyphen and split
    $lastHyphenIndex = $name.LastIndexOf('-')
    if ($lastHyphenIndex -lt 0) { return } # skip if no hyphen

    $prefix = $name.Substring(0, $lastHyphenIndex)
    $suffix = $name.Substring($lastHyphenIndex + 1)

    # Pad numeric suffix to 4 digits
    if ($suffix -match '^\d+$') {
        $padded = $suffix.PadLeft(4, '0')
        $newName = "$prefix-$padded$ext"

        # Rename if name actually changes
        if ($newName -ne $_.Name) {
            Rename-Item $_.FullName -NewName $newName
        }
    }
}
