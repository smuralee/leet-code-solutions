from typing import List


class Codec:

    def encode(self, strs: List[str]) -> str:
        """
        Encodes a list of strings to a single string.
        
        :type strs: List[str]
        :type: str
        """
        res = ''

        for str in strs:
            res += f"{len(str)}|{str}"

        return res

    def decode(self, s: str) -> List[str]:

        res = []
        end = 0
        start = 0
        while end < len(s):

            if s[end].isdigit():
                end += 1

            else:
                length = int(s[start:end])
                res.append(s[end + 1:end + 1 + length])

                end += 1 + length
                start = end

        return res


if __name__ == "__main__":
    strs = ["Helllllllllllllllllo", "World"]
    strs_1 = [""]
    strs_2 = ["", ""]

    codec = Codec()

    print(codec.decode(codec.encode(strs)))
    print(codec.decode(codec.encode(strs_1)))
    print(codec.decode(codec.encode(strs_2)))
