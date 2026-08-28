while True:

    choice1 = input(
        "------------------------------------------------------------------\n"
        "Select calculation:\n"
        "1. Prepare eluent\n"
        "2. Change polarity of the available eluent\n"
        "Enter choice: "
        )

    if choice1 == "1":
        choice2 = input(
        "------------------------------------------------------------------\n"
        "What kind of eluent do you need to prepare?\n"
        "1. Regular Pentane:Ethylacetate mixture?\n"
        "2. Different mixture\n"
        "Enter choice: "
        )

        if choice2 == "1":
            # Ask for data
            p = float(input(
                "------------------------------------------------------------------\n"
                "How many parts of Pentane? "))
            e = float(input(
                "How many parts of Ethylacetate? "))
            v = float(input(
                "What's the needed volume? "))
            # Calculation A
            pentane_result = v * p / (p + e)
            ea_result = v * e / (p + e)

            print("------------------------------------------------------------------\n")
            print("V (pentane): ", f"pentane_result: {pentane_result:.0f}")
            print("V (ethylacetate): ", f"ea_result: {ea_result:.0f}")

            again = input(
                "\nDo you want to make calculations once again?\n"
                "1. Yes\n"
                "2. No\n"
                )

            if again == "1":
                continue

            if again == "2":
                print("Goodbye!")
                break

        if choice2 == "2":
            while True:
                num_words = int(input("How many components? (2-5): "))
                if 2 <= num_words <= 5:
                    break
                print("------------------------------------------------------------------\n"
                    "Please enter a number between 2 and 5.")

            words = []          # create the empty list
            
            for i in range(num_words):
                word = input(f"Enter component {i + 1}: ")
                words.append(word)

            parameters = []     # create the parameter list

            for word in words:
                parameter = int(input(
                    f"How many parts of {word}? "))
                parameters.append(parameter)

            v = float(input(
                "------------------------------------------------------------------\n"
                "What's the volume you need? "))

            sum_parameters = sum(parameters)
            results = []
            for i in range(num_words):
                result = v * parameters[i] / sum_parameters
                results.append(result)

            for i in range(num_words):
                print("------------------------------------------------------------------\n"
                    f"{words[i]}: {results[i]:.0f}"
                )

            again = input(
                "\nDo you want to make calculations once again?\n"
                "1. Yes\n"
                "2. No\n"
                )

            if again == "1":
                continue

            if again == "2":
                print("Goodbye!")
                break
            
    if choice1 == "2":
        choice2 = input(
        "------------------------------------------------------------------\n"
        "What kind of eluent do you have?\n"
        "1. Regular Pentane:Ethylacetate mixture?\n"
        "2. Different mixture\n"
        "Enter choice: "
        )

        if choice2 == "1":
            # Ask for data
            v1 = float(input(
                "------------------------------------------------------------------\n"
                "What's the volume of the eluent do you have? "))
            p1 = float(input(
                "------------------------------------------------------------------\n"
                "How many parts of Pentane in it? "))
            e1 = float(input(
                "------------------------------------------------------------------\n"
                "How many parts of Ethylacetate in it? "))
            p2 = float(input(
                "------------------------------------------------------------------\n"
                "How many parts of Pentane do you need? "))
            e2 = float(input(
                "------------------------------------------------------------------\n"
                "How many parts of Ethylacetate do you need? "))
            v2 = input(
                "------------------------------------------------------------------\n"
                "What's the volume do you need (enter number or 'min' for minimum)? ")
            # Calculation B
            
            if v2 == "min":
                if e2 / (e2 + p2) < e1 / (e1 + p1):
                    pentane_result2 = (v1 * p2 / (p2 + e2) - v1 * p1 / (p1 + e1)) / ( 1 - p2 / (p2 + e2))
                else:
                    pentane_result2 = 0
                if e2 / (e2 + p2) > e1 / (e1 + p1):
                    ea_result2 = (v1 * e2 / (p2 + e2) - v1 * e1 / (p1 + e1)) / ( 1 - e2 / (p2 + e2))
                else:
                    ea_result2 = 0
                    v_result2 = v1 + pentane_result2 + ea_result2

                print("------------------------------------------------------------------\n")
                print("Add into your current eluent:\n")
                print("V (pentane): ", f"pentane_result2: {pentane_result2:.0f}")
                print("V (ethylacetate): ", f"ea_result2: {ea_result2:.0f}")
                print("The total volume will be ", f"v_result2: {v_result2:.0f}")

                again = input(
                    "\nDo you want to make calculations once again?\n"
                    "1. Yes\n"
                    "2. No\n"
                )

                if again == "1":
                    continue

                if again == "2":
                    print("Goodbye!")
                    break
            else:
                v2 = float(v2)
                pentane_result3 = v2 * p2 / (p2 + e2) - v1 * p1 / (p1 + e1)
                ea_result3 = v2 * e2 / (p2 + e2) - v1 * e1 / (p1 + e1)
                v_result3 = v1 + pentane_result3 + ea_result3

                print("------------------------------------------------------------------\n")
                print("Add into your current eluent:\n")
                print("V (pentane): ", f"pentane_result3: {pentane_result3:.0f}")
                print("V (ethylacetate): ", f"ea_result3: {ea_result3:.0f}")
                print("The total volume will be ", f"v_result3: {v_result3:.0f}")

                again = input(
                    "\nDo you want to make calculations once again?\n"
                    "1. Yes\n"
                    "2. No\n"
                )

                if again == "1":
                    continue

                if again == "2":
                    print("Goodbye!")
                    break
        if choice2 == "2":
            print("Unfortunately, you'll have to through away the exsting eluent and make it from the beginning;(")

            again = input(
                "\nDo you want to make calculations once again?\n"
                "1. Yes\n"
                "2. No\n"
            )

            if again == "1":
                continue

            if again == "2":
                print("Goodbye!")
                break