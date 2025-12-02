def has_conflict(stack):
    # check if top choice conflicts with previous choices
    if len(stack) <= 1:
        return False

    top_row, top_col = stack[-1]

    # compare with all queens already placed
    for i in range(len(stack) - 1):
        row, col = stack[i]

        # same column?
        if col == top_col:
            return True

        # diagonal check - if row diff equals col diff then they're diagonal
        if abs(row - top_row) == abs(col - top_col):
            return True

    return False


def solve_n_queens(n):
    # start with queen at row 1 col 1
    stack = [(1, 1)]
    success = False

    while not success and len(stack) > 0:
        # does the newest choice conflict?
        if has_conflict(stack):
            # pop until we find a choice that's not in the last column
            while len(stack) > 0 and stack[-1][1] == n:
                stack.pop()

            # move to next column if stack isn't empty
            if len(stack) > 0:
                row, col = stack.pop()
                stack.append((row, col + 1))

        # no conflict
        else:
            # did we place all n queens?
            if len(stack) == n:
                success = True
            else:
                # add next queen in next row, starting at column 1
                next_row = len(stack) + 1
                stack.append((next_row, 1))

    # print the results
    if success:
        print(f"Solution found for {n}-queens problem:")
        print(f"{'Row':<6} {'Column':<6}")
        print("-" * 15)
        for row, col in stack:
            print(f"{row:<6} {col:<6}")

        # show the board visually
        print(f"\nVisual representation ({n}x{n} board):")
        board = [['.' for _ in range(n)] for _ in range(n)]
        for row, col in stack:
            board[row - 1][col - 1] = 'Q'

        for row in board:
            print(' '.join(row))

        return True
    else:
        print(f"No solution exists for {n}-queens problem.")
        return False


# main program
if __name__ == "__main__":
    print("=" * 50)
    print("N-QUEENS PROBLEM SOLVER")
    print("=" * 50)
    print()

    while True:
        try:
            n = int(input("Enter the number of queens (n): "))

            if n < 1:
                print("Please enter a positive number!\n")
                continue

            print(f"\nSolving for {n} queens on a {n}x{n} board...\n")
            solve_n_queens(n)

            # ask if they want to try again
            print("\n" + "=" * 50)
            again = input(
                "\nDo you want to try another number? (yes/no): ").strip().lower()

            if again not in ['yes', 'y']:
                print("\nThank you for using the N-Queens Solver!")
                break

            print("\n" + "=" * 50 + "\n")

        except ValueError:
            print("Invalid input! Please enter a valid number.\n")
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break
