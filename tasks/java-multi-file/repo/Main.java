public class Main {
    static void check(boolean condition, String message) {
        if (!condition) {
            System.out.println("FAIL: " + message);
            System.exit(1);
        }
    }

    public static void main(String[] args) {
        Account alice = new Account("alice", 10_000);
        Account bob = new Account("bob", 0);

        Bank.transfer(alice, bob, 3_000);
        check(alice.getBalance() == 7_000, "alice should have 7000 after the transfer");
        check(bob.getBalance() == 3_000, "bob should have 3000 after the transfer");

        boolean refused = false;
        try {
            Bank.transfer(alice, bob, 50_000);
        } catch (IllegalStateException e) {
            refused = true;
        }
        check(refused, "a transfer above the balance should throw IllegalStateException");
        check(alice.getBalance() == 7_000, "a refused transfer should not change alice");
        check(bob.getBalance() == 3_000, "a refused transfer should not change bob");
        check(Bank.totalBalance(alice, bob) == 10_000, "money should never be created");

        boolean invalid = false;
        try {
            bob.withdraw(-5);
        } catch (IllegalArgumentException e) {
            invalid = true;
        }
        check(invalid, "a negative amount should throw IllegalArgumentException");

        System.out.println("OK");
    }
}
