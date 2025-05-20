import zipfile

from .file_managers import FileManager, ZipManager
from .text_analyzer import TextAnalyzer
from ..utils.utils import repeating_program
from ..itask import ITask


class Task2(ITask):


    def __init__(self, original_text_path: str, filepath: str, archive_path: str):


        self._text = FileManager.load(original_text_path)
        self._string_handler = TextAnalyzer()
        self._final_text = ''
        self._file_path = filepath
        self._archive_path = archive_path

    @repeating_program
    def run(self):

        try:
            self._calculate_results()

            FileManager.save(self._final_text, self._file_path)
            ZipManager.save(self._file_path, self._archive_path)

            text = ZipManager.load(self._archive_path, self._file_path.split('/')[-1])
            print(f'Text from archive:\n{text}')

            info = ZipManager.file_info(self._archive_path, self._file_path.split('/')[-1])
            print(f'Information about file:\n{self._file_info(info)}')
        except Exception as e:
            print(e)

    def _calculate_results(self):

        sentence_count = len(self._string_handler.sentences(self._text))
        every_sentences_count = self._string_handler.count_of_every_sentence_type(self._text)
        average_word_length_in_sentence = tuple(self._string_handler.average_sentence_length(self._text))
        average_word_length_in_text = round(sum(average_word_length_in_sentence) / sentence_count, 2)
        smileys_count = len(self._string_handler.get_smileys(self._text))
        phone_numbers = self._string_handler.get_phone_numbers(self._text)
        let = self._string_handler.check_letters(self._text)
        avg_len, avg_words, seventh_words = self._string_handler.analyze_text(self._text)
        words_with_last_consonant = self._string_handler.count_words_ending_with_consonant(self._text)
        words = self._string_handler.get_words(self._text)

        self._final_text += f'Number of sentences in the text: {sentence_count}\n' + \
                            f'Number of declarative, interrogative, and exclamatory sentences: ' + \
                            f'{every_sentences_count}\n' + \
                            f'Average sentence length in characters: {round(len(words)*sum(average_word_length_in_sentence)/(len(average_word_length_in_sentence)*sentence_count))}\n' + \
                            f'Average word length in the text in characters: {average_word_length_in_text}\n' + \
                            f'Number of smileys: {smileys_count}\n' + \
                            f'Phone numbers: {phone_numbers}\n' + \
                            f'2th letter is vowel and 3th is consonant: {let}\n' + \
                            f'Count words with last consonant: {words_with_last_consonant}\n' + \
                            f'Average word length: {avg_len}\n' + \
                            f'Such words: {avg_words}\n' if avg_words else 'No sush words\n' + \
                            f'Every 7th word: {seventh_words}\n'

    @staticmethod
    def _file_info(info: zipfile.ZipInfo):

        return (f'Original size: {info.file_size} bytes. '
                f'\nCompressed size: {info.compress_size} bytes')
