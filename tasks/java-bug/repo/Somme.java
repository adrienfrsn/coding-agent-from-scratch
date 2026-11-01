public class Somme {
    static int somme(int[] valeurs) {
        int total = 0;
        for (int i = 1; i < valeurs.length; i++) {
            total += valeurs[i];
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(somme(new int[] {1, 2, 3, 4}));
    }
}
