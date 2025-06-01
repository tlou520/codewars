#Name challenge: Breaking the Vigenère Cipher
#https://www.codewars.com/kata/544e5d75908f2d5eb700052b
import string
import matplotlib.pyplot as plt
import pandas as pd


from collections import Counter


letters_value = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
    'M': 12,
    'N': 13,
    'O': 14,
    'P': 15,
    'Q': 16,
    'R': 17,
    'S': 18,
    'T': 19,
    'U': 20,
    'V': 21,
    'W': 22,
    'X': 23,
    'Y': 24,
    'Z': 25
}

value_letters = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z'
}

F_i = {
    "A": 0.082, "B": 0.014, "C": 0.028, "D": 0.038, "E": 0.131,
    "F": 0.029, "G": 0.020, "H": 0.053, "I": 0.064, "J": 0.001,
    "K": 0.004, "L": 0.034, "M": 0.025, "N": 0.071, "O": 0.080,
    "P": 0.020, "Q": 0.001, "R": 0.068, "S": 0.061, "T": 0.105,
    "U": 0.025, "V": 0.009, "W": 0.015, "X": 0.002, "Y": 0.020,
    "Z": 0.001
}

class Cosets:
    def __init__(self):
        self.cosets = []
        self.frequencies_df = pd.DataFrame()
        self.chi_squared_df = pd.DataFrame()
        self.shifts_minimums = pd.DataFrame()


    def divide_into_cosets(self, text: str, n_length: int) -> None:
        if not text.isupper():
            raise ValueError("Input text must be in all uppercase.")
        if n_length <= 0:
            raise ValueError("n_length must be a positive integer.")

        self.cosets = ['' for _ in range(n_length)]
        for index, char in enumerate(text):
            self.cosets[index % n_length] += char

    def get_cosets(self) -> list[str]:
        return self.cosets
    
    def divide_into_cosets(self, text: str, n_length: int) -> None:
        if not text.isupper():
            raise ValueError("Text must be all uppercase.")
        if n_length <= 0:
            raise ValueError("n_length must be a positive integer.")

        self.cosets = ['' for _ in range(n_length)]
        for i, char in enumerate(text):
            self.cosets[i % n_length] += char

        self.frequencies_df = pd.DataFrame([Counter(c) for c in self.cosets]).fillna(0).astype(int)

    def extract_row_minima_with_labels(self) -> None:
        """
        For each coset (row) in self.chi_squared_df, compute both:
          - the minimum chi‐squared value across all shifts, and
          - the name of the shift column where that minimum occurs.
        
        Returns
        -------
        pandas.DataFrame
            A DataFrame with columns ['min_value', 'min_shift'], indexed by coset.
        """
        min_values = self.chi_squared_df.min(axis=1)
        min_shifts = self.chi_squared_df.idxmin(axis=1)
        
        self.min_chi_results = pd.DataFrame({
            'min_value': min_values,
            'min_shift': min_shifts
        })


    def _shift_text(self, text: str, shift: int) -> str:
        shifted = []
        for ch in text:
            if 'A' <= ch <= 'Z':
                shifted.append(value_letters[(letters_value[ch] - shift) % 26])
        return ''.join(shifted)

    def compute_chi_squared_table(self) -> None:
        chi_data = []

        for coset in self.cosets:
            row = []

            for shift in range(26):
                shifted = self._shift_text(coset, shift)
                observed = Counter(shifted)

                chi_sq = 0.0
                for ch in string.ascii_uppercase:
                    f_i = observed.get(ch, 0) / len(shifted)
                    chi_sq += ((f_i - F_i[ch]) ** 2) / F_i[ch]
                row.append(chi_sq)

            chi_data.append(row)

        self.chi_squared_df = pd.DataFrame(chi_data, columns=[f"Shift_{s}" for s in range(26)])
        self.extract_row_minima_with_labels()


    def return_possible_key(self) -> str:
        shift_letters = ""
        num = 0
        for shift in self.min_chi_results['min_shift']:
            num = int(shift[6:])
            shift_letters += value_letters[num]

        return shift_letters


def decrypt(text: str, possible_key: str) -> str:
        result = ""
        i = 0
        while i < len(text):
            j = 0
            while j < len(possible_key):
                if i >= len(text):
                    break
                result += value_letters[(letters_value[text[i]] - letters_value[possible_key[j]]) % 26]
                j += 1
                i += 1

        return result


def get_keyword(ciphertext: str, key_len: int) -> str:
    #Dividing the ciphertext into cosets
    c = Cosets()
    c.divide_into_cosets(ciphertext, key_len)
    #Finding the smallest Chi Square of every shift in every coset
    c.compute_chi_squared_table()
    print(c.get_cosets())
    possible_key = c.return_possible_key()
    return possible_key


def main():
    # Your main logic here
    ciphertext = "NSWXARWJGEXIJCZWUZLOAWFJFTUIMUVFEWHWPEEVVCYENYSGVVECSRZLGFDRZBPKWPMIYTFFGQDRJOKOTWWIWNVKUOBEXOLLZFDCOWZLJCXXQSZFITUIMUVFVLVEJDKZGSVWWYNANZKERERFKRLSOYEUTOWMYLVLVSUJNEHMGBFCEFKZGSVWWYZKCPRYPTYWHFHUQEELWGHSBXISAGWSPRVSVNHFNAJAPEDXWRUAHTHVANKSWHKSNSYSXSKEXIKKYVLGDCRFDSUIBLVUVSGMJTYWKFXWAOWDGHWINSYWOWQKSAPKYFLXENXKVMOIBOIWZOPTHEZKXWVMXLPVKTIINEELHFRQBALDMBHVOLVLVSUFEGISOHUMCRREYCUHBRVIWSQGEEJOQFGPANXLJOQHOEELGBFIHEEYVVFEJBVUCZFYHAKWFTRVOPVUKTLGWUKZQFVEJDLKGRWSLRFNGCUHESGJQJHEQTYGTGKMLOWLGLWWAVVFHCUEQTYGTGZLKSVKVMOIOAIWPCWWKDZNGFJIJTRUEIUEPERNGFDKALVLVSUJNEHMGBFMASTSPCQPUBVYNSDRADSQCBDPUZZFIOOENGVSOCXRPOWJGDUIOEELCHLZATVPVKLXDTYWCJDMHASANWWCKFDGFSURYODHWHLRCAEVECOPACKAQBVSBLRJISWITTTGTDRVWSLUJQDPYUCSVWRROAIWGOVMHYDSFSHBWMGDGGFEJBVVTOZRBRFECJDVEEKQQTVSQRTWUDUIOSIWRCUXENXJGZLKEOLKVSAXOSTAGBWMBITLGLWWWNUYGBHVWLWAEHLSJAEVVVHVAAIWFWIJARVFESVIOPVUKOOPUFFJISQINACXKQWMKNNAVVWLAPFKKHLSJOWZCBGMSIKZJPHGKMZFIARVACFEOCQLARSWTHVDEMZFJWVGHAJKKQLRPRFVWQWSNYTJADWSCRRHJMWITTTGFSVEJDJWEFHXSRZLKBJKEVVKVVHIJGCAUVOIPTVJHFHUQEEUAGHUQEEUGOVIPAFFTWVLZLWUOIJCLWSNMXAUVTYWOCVXYODEQBOIPTVJROLVOAJLJVHEJRVWTWQSJAKFFGWIOEEGHHHIZOILKVLEOTFSPRWLAMFKVQRQIOEVQIEPADCWVHHVOAJDNSHWOOFLVTIVNNEHRQFXDEKGRHZIHVVDGHWINSTGODUMOERTQIWSBTYWVCWEHUJSISWLATFHGWJLPLVLVSUWYODHTWVIWBFMVCIXDEKGVOOYOAXWNSWXARWJGEXIJCPSUOIYJCKAQBRJNAECEOQFAFZLVSGAALCTAGHZARRDTOQOBUEUVWRROWZLJHKIPWFHCFDQATVJECFLKBVLCFDRGFLFEHLSJBVAPUWLABVKVOQSPHVJTOQOBUEUVWRRSIKZPCDHFUJLCPOIBRVWROUEIEKWTOOWKFZLUHKIHEKLGFIVAQLWPQBHESKJKPXXEOEJGOVSJASDAKHPHTYWUOPIBUEUVWRRDAJTGSQYOEULQTLXPHVSOWQSWCZVHFHUQEEUAWQTNOKWKBVIMUVFESVEOPPMUWQKPHVNKQFMLHVJQFVSIEFLJSUGEPYWTPDWADFFCGWVWDUDKBJGDETCGFESWRULADLGWLCQWGHWWMEWOCQMYSLUJOVEOIELQSUVZRFHRWQKPHVKGQRRZRKGTSPIIBVJVVHXKPVAIVWGDAISEHHVOTYWWGHSBLVLVSUJNEHMGBFMASRFFTUIMUVFEMDRWLPKKGSPWYJSHIQHWMVFVOOVKLVAPQUCLTFYTOPWWNUKGJHVWLNGTRSYVZCWIOPIOIEUNIGMJGYSPUPEJSTJCPEPAAEVVVHXALVNKGLSJGREGGKSSWYWGZRJBOILWBHSJEFXVVHIWRCAGGWHASTJKDWMKNZFEZDWOITSNZLXARRLWFHSBAGHNMLRCTYWMBRAHEUYGCIIJGCAUVOIPTVJHFHUQEEUAHRWKLMAPUDGNYGLQUUEIIJXQIQHENVSRCHWBADGWGVXKRPLJSJSHDSMIKKINEKZGAHXDOUAUGXGYEJKHIOPUAGHNWHHPOUWEWSLARREGGVECEZFUHUYYTZFICQXDENZGFHEXOLLUCIEPRVSUIUIDIUVGBECYAGLCWQOEDUDGHWINFIWSIHRYIVKJOGEOTIGPUHJBETLQBWLADVKKUQSBSFEGYHCXORJFZDCKUKKVVHQKSKXTSTYANKDGHWINSRJGCQXDESGVHRQNONGHHKIXLZUMSQWZEIXGFWCLENJKHHVWNULJSKSIEIGYCIXDEUNQFDOOIDHNWIMADBWAPREND"
    key_len = len("CODEWARS")
    #ciphertext = "NWAIWEBBRFQFOCJPUGDOJVBGWSPTWRZ"
    #key_len = len("BOY")
    get_keyword(ciphertext, key_len)

if __name__ == "__main__":
    main()
