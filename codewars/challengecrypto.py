# Name of the challenge: Hide a message in a deck of playing cards
#Link: https://www.codewars.com/kata/59b9a92a6236547247000110


from typing import Dict, List

class PlayingCards:
    fact = [
                1,
                1,
                2,
                6,
                24,
                120,
                720,
                5040,
                40320,
                362880,
                3628800,
                39916800,
                479001600,
                6227020800,
                87178291200,
                1307674368000,
                20922789888000,
                355687428096000,
                6402373705728000,
                121645100408832000,
                2432902008176640000,
                51090942171709440000,
                1124000727777607680000,
                25852016738884976640000,
                620448401733239439360000,
                15511210043330985984000000,
                403291461126605635584000000,
                10888869450418352160768000000,
                304888344611713860501504000000,
                8841761993739701954543616000000,
                265252859812191058636308480000000,
                8222838654177922817725562880000000,
                263130836933693530167218012160000000,
                8683317618811886495518194401280000000,
                295232799039604140847618609643520000000,
                10333147966386144929666651337523200000000,
                371993326789901217467999448150835200000000,
                13763753091226345046315979581580902400000000,
                523022617466601111760007224100074291200000000,
                20397882081197443358640281739902897356800000000,
                815915283247897734345611269596115894272000000000,
                33452526613163807108170062053440751665152000000000,
                1405006117752879898543142606244511569936384000000000,
                60415263063373835637355132068513997507264512000000000,
                2658271574788448768043625811014615890319638528000000000,
                119622220865480194561963161495657715064383733760000000000,
                5502622159812088949850305428800254892961651752960000000000,
                258623241511168180642964355153611979969197632389120000000000,
                12413915592536072670862289047373375038521486354677760000000000,
                608281864034267560872252163321295376887552831379210240000000000,
                30414093201713378043612608166064768844377641568960512000000000000,
                1551118753287382280224243016469303211063259720016986112000000000000
    ]  

    Deck_cards = [
                "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
                "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
                "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "TH", "JH", "QH", "KH",
                "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "TS", "JS", "QS", "KS"
            ]
    custom_order= {
        "AC": 0,
        "2C": 1,
        "3C": 2,
        "4C": 3,
        "5C": 4,
        "6C": 5,
        "7C": 6,
        "8C": 7,
        "9C": 8,
        "TC": 9,
        "JC": 10,
        "QC": 11,
        "KC": 12,
        "AD": 13,
        "2D": 14,
        "3D": 15,
        "4D": 16,
        "5D": 17,
        "6D": 18,
        "7D": 19,
        "8D": 20,
        "9D": 21,
        "TD": 22,
        "JD": 23,
        "QD": 24,
        "KD": 25,
        "AH": 26,
        "2H": 27,
        "3H": 28,
        "4H": 29,
        "5H": 30,
        "6H": 31,
        "7H": 32,
        "8H": 33,
        "9H": 34,
        "TH": 35,
        "JH": 36,
        "QH": 37,
        "KH": 38,
        "AS": 39,
        "2S": 40,
        "3S": 41,
        "4S": 42,
        "5S": 43,
        "6S": 44,
        "7S": 45,
        "8S": 46,
        "9S": 47,
        "TS": 48,
        "JS": 49,
        "QS": 50,
        "KS": 51
    }
    letter_value: Dict[str, int] = {
        ' ': 0, 'A': 1,  'B': 2,  'C': 3,  'D': 4,  'E': 5,  'F': 6,  'G': 7,
        'H': 8,  'I': 9,  'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14,
        'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21,
        'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26
    }

    value_letter: Dict[int, str] = {
    0: ' ', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G',
    8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N',
    15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U',
    22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'
}

    def output(self, indices):
        mapped = [str(self.Deck_cards[i]) for i in indices]
        print(mapped)
        return mapped

    def string_to_base27_value(self, s: str) -> int:
        """
        Converts an uppercase letter string into its decimal value
        when interpreted as a base‑27 number with A=1, B=2, …, Z=26.

        Parameters:
            s (str): The input string composed of letters A–Z.

        Returns:
            int: The corresponding decimal value.
        """
        total: int = 0
        for position, char in enumerate(reversed(s)):
            # The letter’s numeric value is retrieved; zero is used if absent
            value: int = self.letter_value.get(char, 0)
            total += value * (27 ** position)
        return total

    def custom_key(self, card):
        return self.custom_order[card]
    
    def ith_permutation(self, n: int, i: int) -> list[int]:
        # Compute factorial numbers

        # Compute factorial code
        perm = [0] * n
        for k in range(n):
            perm[k] = i // self.fact[n - 1 - k]
            i = i % self.fact[n - 1 - k]

        # Readjust values to obtain the permutation
        for k in range(n - 1, 0, -1):
            for j in range(k - 1, -1, -1):
                if perm[j] <= perm[k]:
                    perm[k] += 1

        return perm

    # Takes a String containing a message, and returns an array of Strings representing
    # a deck of playing cards ordered to hide the message
    def encode(self, message):
        number_encoded = self.string_to_base27_value(message)
        indices = self.ith_permutation(52, number_encoded)
        output = self.output(indices)
        return output
    
    def index_of_permutation(self, perm: List[int]) -> int:
        """
        Given a permutation of the numbers 0 to 51 (inclusive),
        return its lexicographic index in the list of all 52! permutations.
        """
        n = len(perm)
        if sorted(perm) != list(range(n)):
            raise ValueError("Input must be a permutation of integers from 0 to 51")

        used = [False] * n
        index = 0

        for k, p_k in enumerate(perm):
            smaller = sum(1 for x in range(p_k) if not used[x])
            index += smaller * self.fact[n - 1 - k]
            used[p_k] = True

        return index

    def array_in_numbers(self, deck):
        # Create a mapping from card to index
        indexed_array = [self.Deck_cards.index(card) for card in deck]
        
        return indexed_array

    def string_from_value(self, N: int) -> str:
        """
        Converts the integer N into a base-27 representation, mapping each digit
        0–26 into its corresponding character (0 → space, 1 → 'A', …, 26 → 'Z').
        Returns the resulting string, most significant digit first.
        """
        if N < 0:
            raise ValueError("N must be non-negative")
        # Special case for zero
        if N == 0:
            return ''

        digits: list[str] = []
        # Extract digits least significant first
        while True:
            d = N % 27
            digits.append(self.value_letter[d])
            N //= 27
            if N == 0:
                break
        # Reverse to obtain most significant first
        return ''.join(reversed(digits))
  

    def printDeck(self, Index):
        result = self.string_from_value(Index)
        return result
        
    # Takes an array of Strings representing a deck of playing cards, and returns
    # the message that is hidden inside
    def decode(self, deck):
        ArrayNumbers = self.array_in_numbers(deck)
        Index = self.index_of_permutation(ArrayNumbers)
        final = self.printDeck(Index)
        return final


def main():
    playingCards = PlayingCards()
    playingCards.decode(["AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC", "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD", "AH", "2H", "3H", "4H", "8H", "9S", "3S", "2S", "8S", "TS", "QS", "9H", "7H", "KH", "AS", "JH", "4S", "KS", "JS", "5S", "TH", "7S", "6S", "5H", "QH", "6H"])


if __name__ == "__main__":
    main()