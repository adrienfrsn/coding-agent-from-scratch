public class Sum {
    static int sum(int[] values) {
        int total = 0;
        for (int i = 1; i < values.length; i++) {
            total += values[i];
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(sum(new int[] {1, 2, 3, 4}));
    }
}
