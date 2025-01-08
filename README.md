# Cipher Text Decryption Program

## Overview
This program is designed to decrypt cipher text files using a series of frequency analysis and pattern-matching techniques. It employs multiprocessing to improve performance and processes cipher text in stages to identify and replace characters based on common English letter frequencies, bigrams, trigrams, and word structures.

## Features
1. **Punctuation Removal:** Removes all non-English letters and non-alphabetical characters from the cipher text.
2. **Frequency Analysis:** Counts letter frequency to identify common English letters like 'E'.
3. **Pattern Matching:** Matches cipher text letters to common English words and patterns (e.g., "THE", "ING", "ABLE").
4. **Parallel Processing:** Utilizes multiprocessing for better performance.
5. **Incremental Decoding:** Gradually decodes the cipher text by replacing letters and updating the text iteratively.
6. **Key Output:** Saves the substitution key to a file.
7. **Decrypted Text Output:** Outputs the decrypted text to a separate file.

## Input and Output
### Input:
- A text file containing the encrypted message.
- Supporting files containing common two-, three-, four-, and five-letter words (e.g., `most_freq_two_letter.txt`).

### Output:
- **Key File:** Contains the mapping of cipher text letters to decrypted letters.
- **Decrypted File:** Contains the fully or partially decrypted text.

## How It Works
1. **Input Cipher Text:**
   - The program reads the cipher text from the specified file.
   - Converts the text to lowercase for uniform processing.

2. **Frequency Analysis:**
   - Counts letter frequencies to identify the most common letters (e.g., 'E', 'T', 'A').

3. **Pattern Matching:**
   - Uses predefined patterns (e.g., "THE", "ING", "ABLE") to identify likely substitutions.
   - Identifies bigrams and trigrams for further decoding.

4. **Multiprocessing:**
   - Runs decoding processes in parallel to improve performance.

5. **Incremental Replacement:**
   - Replaces letters in the cipher text iteratively, updating the text at each step.

6. **Output Results:**
   - Saves the substitution key and the decrypted text to their respective files.

## Files
- **Input File:** The cipher text file provided by the user.
- **Supporting Word Files:**
  - `most_freq_two_letter.txt`
  - `most_freq_three_letter.txt`
  - `most_freq_four_letter.txt`
  - `most_freq_five_letter.txt`
- **Output Files:**
  - `<input_filename>-key.txt`: Contains the mapping of cipher letters to decrypted letters.
  - `<input_filename>-decrypted.txt`: Contains the decrypted text.

## Usage
1. Place the encrypted file and supporting word files in the same directory as the script.
2. Run the script:
   ```bash
   python <script_name>.py
   ```
3. Enter the name of the cipher text file when prompted.

### Example:
```bash
Please enter filename wish to decrypt: encrypted_message.txt
Finished in 10.5 second(s)
Keys saved in file: encrypted_message-key.txt
Decrypted text saved in file: encrypted_message-decrypted.txt
```

## Dependencies
- Python 3.x
- Multiprocessing library (built into Python)

## Code Structure
### Main Functions:
1. **strip_punctuation:** Removes all unwanted characters from the cipher text.
2. **frequency_analysis:** Analyzes the frequency of letters in the text.
3. **single_letter & single_letter_word:** Identifies and replaces single letters based on frequency and context.
4. **bigram and trigram functions:** Match common English patterns like "TH", "ING", and "ABLE".
5. **double_two_letters:** Identifies and replaces repeating letters (e.g., "EE", "LL").
6. **ending_LY & ending_ABLE:** Decodes words with specific suffixes (e.g., "LY", "ABLE").

### Parallel Processes:
- Processes run independently to analyze and replace specific patterns concurrently.

## Known Limitations
1. **Partial Decryption:** If the cipher text deviates significantly from standard English patterns, the output may be incomplete.
2. **Resource Usage:** Multiprocessing may consume significant resources for very large files.

## Future Enhancements
1. **Improved Pattern Matching:** Incorporate more complex linguistic rules for better accuracy.
2. **Dynamic Learning:** Use machine learning to adapt to different cipher text structures.
3. **GUI Integration:** Add a graphical interface for ease of use.

## License
This program is open-source and available under the MIT License.

## Author
Developed by [Your Name].
