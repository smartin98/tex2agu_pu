import re
import os
import argparse

class AGUManuscriptPUCalculator:
    def __init__(self, latex_file):
        self.latex_file = latex_file

    def count_words(self, text):
        """Counts the number of words in a given text."""
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def extract_text(self):
        """Extracts relevant text from the LaTeX file."""
        with open(self.latex_file, 'r') as file:
            content = file.read()

        # Remove everything before \begin{abstract} (the preamble)
        content = content.split('\\begin{abstract}', 1)
        if len(content) > 1:
            content = content[1]
        else:
            raise ValueError("The LaTeX file does not contain a \\begin{document} command.")

        # Remove LaTeX comments
        content = re.sub(r'%.*', '', content)

        # Remove title, authors, affiliations, key points, keywords
        content = re.sub(r'\\title\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\author\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\affil\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\keywords\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{keypoints\}.*?\\end\{keypoints\}', '', content, flags=re.DOTALL)

        # Extract main body text (exclude references and text in tables)
        content = re.sub(r'\\begin\{thebibliography\}.*', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{table\}.*?\\end\{table\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{longtable\}.*?\\end\{longtable\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{equation\}.*?\\end\{equation\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{equation\*\}.*?\\end\{equation\*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{align\}.*?\\end\{align\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{align*\}.*?\\end\{align*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\label\{.*?\}', '', content, flags=re.DOTALL)

        # Remove figure environments but count them separately
        figure_count = len(re.findall(r'\\begin\{figure\*?\}(?:\[.*?\])?.*?\\end\{figure\*?\}', content, flags=re.DOTALL))
        content = re.sub(r'\\begin\{figure\*?\}(?:\[.*?\])?.*?\\end\{figure\*?\}', '', content, flags=re.DOTALL)

        content = re.sub(r'\\begin\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\end\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\cite\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\citeA\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\ref\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\ref\{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\\w+', '', content)
        
        return content, figure_count

    def calculate_publication_units(self):
        """Calculates the publication units based on word count and figures/tables."""
        content, figure_count = self.extract_text()
        word_count = self.count_words(content)

        # Calculate publication units
        word_pus = word_count / 500
        total_pus = word_pus + figure_count

        return word_count, figure_count, total_pus



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--tex_path', type = str, help = 'file path of latex file')
    parser.add_argument('--verbose', action='store_true', help='option to print extracted text for debugging')
    args = parser.parse_args()
    
    # Example usage
    if args.tex_path is None:
        raise ValueError("must provide tex file path using --tex_path option")
    else:
        latex_file = args.tex_path

    if not os.path.exists(latex_file):
        print(f"Error: File '{latex_file}' not found.")
    else:
        calculator = AGUManuscriptPUCalculator(latex_file)
        word_count, figure_count, total_pus = calculator.calculate_publication_units()

        if args.verbose:
            print("Extracted Text:")
            content,_ = calculator.extract_text()
            print(content)

        print("Manuscript Length Calculation:")
        print(f"Word Count (excluding title, authors, etc.): {word_count}")
        print(f"Number of Figures: {figure_count}")
        print(f"Total Publication Units (PU): {total_pus:.2f}")
