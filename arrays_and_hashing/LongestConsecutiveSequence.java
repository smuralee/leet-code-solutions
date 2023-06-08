import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

class LongestConsecutiveSequence {

    public static void main(String[] args) {
        LongestConsecutiveSequence solution = new LongestConsecutiveSequence();

        solution.longestConsecutive(new int[]{100, 4, 200, 1, 3, 2});
        solution.longestConsecutive(new int[]{0, 3, 7, 2, 5, 8, 4, 6, 0, 1});
    }

    public void longestConsecutive(int[] inputArray) {

        // Convert to the collection to use .contains function and sorting
        Set<Integer> inputSet = new HashSet<>();
        Arrays.stream(inputArray)
                .forEach(inputSet::add);

        // Initialize the count of the longest sequence
        int longestCount = 0;

        // Loop through the set
        for (int number : inputSet) {
            /*
             * Check if the previous number is existing in the collection
             * If not, initialize current number and set the sequence count as 1
             */
            if (!inputSet.contains(number - 1)) {
                int currentNumber = number;
                int currentCount = 1;

                /*
                 * Keep checking till the next consecutive number if found
                 * Increment the marker on the current number
                 * i.e. if 1 was found, increment to 2, check if 2 exists then increment to 3, continue till the sequence is broken
                 * Increment the count of the sequence
                 */
                while (inputSet.contains(currentNumber + 1)) {
                    currentNumber += 1;
                    currentCount += 1;
                }

                /*
                 * Once the sequence is broken, find the max of the current and longest count
                 * Store that value in the longest count
                 */
                longestCount = Math.max(longestCount, currentCount);
            }
        }

        System.out.println("Longest consecutive sequence is : " + longestCount);
    }
}

