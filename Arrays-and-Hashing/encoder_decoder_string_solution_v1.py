from typing import List


class Codec:

    def encode(self, strs: List[str]) -> str:
        """
        Encodes a list of strings to a single string.
        
        :type strs: List[str]
        :rtype: str
        """
        string = ''
        string_length = ''
        length = 0
        for stri in strs:
            string += stri
            string_length += str(len(stri)) + '-'
            length += len(stri)

        res = string + string_length + str(length)
        # print(f'encoder output {res}')
        return res

    def decode(self, s):
        """
        Decodes a single string to a list of strings.
        
        :type s: str
        :rtype: List[str]
        """
        res = [""]

        # O(n)
        length = int(s.split('-')[-1])

        #  O(n)
        string_length = s[length:-1]
        string_length = string_length.split('-')[:-1]

        # print(string_length)

        string = s[:length]
        # print(string)

        counter = 0
        for i in range(len(string_length)):

            if string_length[i] == str(0):
                res.append("")
            else:
                res.append(string[counter: counter + int(string_length[i])])
                counter += int(string_length[i])

        return res[1:]


if __name__ == "__main__":
    strs = ["Helllllllllllllllllo", "World"]
    strs_1 = [""]
    strs_2 = ["", ""]

    codec = Codec()

    print(codec.decode(codec.encode(strs)))
    print(codec.decode(codec.encode(strs_1)))
    print(codec.decode(codec.encode(strs_2)))
