import re


class TextAnalyzer(object):

    @staticmethod
    def sentences(text: str):
        punctuators = re.split(r'[.!?]+(?=\s+|$)', text)
        punctuators.pop()
        return punctuators

    @staticmethod
    def count_of_every_sentence_type(text: str):
        punctuators = ('.', '?', '!')
        return tuple(len(re.findall(fr'[{p}]+(?=\s+|$)', text)) for p in punctuators)

    @staticmethod
    def average_sentence_length(text: str):
        sentences = TextAnalyzer.sentences(text)

        for sentence in sentences:
            words = TextAnalyzer.get_words(sentence)
            yield round(sum(map(len, words)) / len(words), 2)

    @staticmethod
    def get_words(text: str):

        return re.findall(r'\b[а-яА-Я]+\b', text)

    @staticmethod
    def analyze_text(text: str) -> tuple[int, list[str], list[str]]:

        words = re.findall(r'\b[а-яА-ЯёЁ]+\b', text)
        
        avg_len = round(sum(len(w) for w in words) / len(words))
        
        avg_words = re.findall(rf'\b[а-яА-ЯёЁ]{{{avg_len}}}\b', text)
        
        seventh_words = words[6::7]
        
        return avg_len, avg_words, seventh_words

    @staticmethod
    def get_words_with_len(text: str, length: int):

        return re.findall(fr'\b[а-яА-Я]{{{length}}}\b', text)

    @staticmethod
    def get_smileys(text: str):

        return re.findall(r'((?<=\s)[:;]-*([()\[\]])\2*(?=\s+))', text)

    @staticmethod
    def get_phone_numbers(text: str):

        return re.findall(r'\b29\d{7}\b', text)

    @staticmethod
    def check_letters(text: str):
        
        return re.findall(r'\b\w[бвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩ][аеёиоуыэюяАЕЁИОУЫЭЮЯ]\w*\b', text)
    
    @staticmethod
    def count_words_ending_with_consonant(text: str) -> int:

        consonant_pattern = r'[бвгджзйклмнпрстфхцчшщъьБВГДЖЗЙКЛМНПРСТФХЦЧШЩЪЬ]'

        words = re.findall(rf'\b\w+{consonant_pattern}\b', text, flags=re.IGNORECASE)
    
        return len(words)
