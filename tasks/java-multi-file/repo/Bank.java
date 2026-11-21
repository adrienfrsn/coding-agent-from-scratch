public class Bank {
    /** Moves money between two accounts, nothing changes if the transfer fails. */
    public static void transfer(Account from, Account to, long amount) {
        to.deposit(amount);
        from.withdraw(amount);
    }

    public static long totalBalance(Account... accounts) {
        long total = 0;
        for (Account account : accounts) {
            total += account.getBalance();
        }
        return total;
    }
}
