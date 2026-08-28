import math


while True:

    choice1 = input(
        "------------------------------------------------------------------\n"
        "Select calculation:\n"
        "1. Eluent predictor (at least one TLC is needed)\n"
        "2. Runing a flash column\n"
        "3. Prepare eluent\n"
        "4. Change polarity of eluent\n"
        "Enter choice: "
        )
    if choice1 == "1":
        choice2 = input(
        "------------------------------------------------------------------\n"
        "What kind of eluent do work with?\n"
        "1. Regular Pentane:Ethylacetate mixture?\n"
        "2. Different mixture\n"
        "Enter choice: "
        )

        if choice2 == "1":
            # Ask for data
            r1 = float(input(
                "------------------------------------------------------------------\n"
                "What's the Rf value of the product based on TLC (between 0.01 and 0.99) ? "))
            p1 = float(input(
                "How many parts of Pentane? "))
            e1 = float(input(
                "How many parts of Ethylacetate? "))
            r2 = float(input(
                "What's the Rf value do you need for your product (between 0.01 and 0.99) ? "))
            # Calculation A
            x = -e1 / ((e1 + p1) * math.log(1 - r1))
            u2 = -x * math.log(1 - r2)
            if u2 <= 0.5:
                pentane_result2 = 1 / u2 - 1
                ea_result2 = 1
            else:
                x = -p1 / ((e1 + p1) * math.exp(1 - r1))
                u2 = -x * math.exp(1 - r2)
                pentane_result2 = 1
                ea_result2 = 1 / u2 - 1
            print("------------------------------------------------------------------\n")
            print("You should try to do TLC with the eluent consists of:\n")
            print(f"V (pentane): {pentane_result2:.0f}")
            print(f"V (ethylacetate): {ea_result2:.0f}")

            again = input(
                "\nDo you want to go to the main menu? \n"
                "1. Yes\n"
                "2. No\n"
                )

            if again == "1":
                continue

            if again == "2":  
                print("------------------------------------------------------------------\n"
                "QuickFC v.1.3, Flash Column Chromatography Calculator."
                "© 2024-2026 Dmitrii Ladan. All rights reserved. \n"
                "Goodbye!")
                break

        if choice2 == "2":
            print("Unfortunately, I cannot help you;( ")






    if choice1 == "2":
        choice2 = input(
        "------------------------------------------------------------------\n"
        "Do you know what the column size you're gonna to use?\n"
        "1. Yes\n"
        "2. No\n"
        "Enter choice: "
        )




        if choice2 == "1":
            # Ask for data
            D = float(input(
                "What's the D (internal column diameter) (mm) ? "))
            L = float(input(
                "What's the L (column length) (cm) ? "))
            Rfmin = float(input(
                "What's the lowRf (the lowest Rf value of the needed compound) ? "))
            # Calculation A
            ms = math.pow((D / 20), 2) * 3.14 * L * 0.5
            Vd = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 1.5 / Rfmin
            Vsl = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 0.8
            Vw = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 1.5 / Rfmin - Vsl

            n1 = Vw/10
            n2 = Vw/20


            print("------------------------------------------------------------------\n")
            print(f"For the choisen column of D = {D:.0f}mm and L = {L:.0f}cm")

            print(" \n")

            print("Dry silica loading:")
            print(f"Volume of eluent for colomning (ml): {Vd:.0f}")

            print(" \n")

            print("Wet silica loading:")
            print(f"Volume of eluent for wet loading of silica (ml): {Vsl:.0f}")
            print(f"Volume of eluent for colomning (ml): {Vw:.0f}")

            print(" \n")

            print(f"Number of 10ml test tubes (small): {n1:.0f}")
            print(f"Number of 20ml test tubes (large): {n2:.0f}")

            again = input(
                "------------------------------------------------------------------\n"
                "\nDo you want to go to the main menu? \n"
                "1. Yes\n"
                "2. No\n"
                )

            if again == "1":
                continue

            if again == "2":  
                print("------------------------------------------------------------------\n"
                "QuickFC v.1.3, Flash Column Chromatography Calculator."
                "© 2024-2026 Dmitrii Ladan. All rights reserved. \n"
                "Goodbye!")
                break




        if choice2 == "2":
            # Ask for data
            m = float(input(
                "------------------------------------------------------------------\n"
                "What's the m (mass of your sample) (mg) ? "))
            dRf = float(input(
                "What's the dRf (difference in Rf values between the spot of the needed compound and the closest one) ? "))
            Rfmin = float(input(
                "What's the lowRf (the lowest Rf value of the needed compound) ? "))
            L = float(input(
                "What's the L (column length) (cm) (if don't know, set maximum which is about 25) ? "))
            # Calculation A
            D = m / (2 * math.sqrt(m / 10)) * 0.1 / math.pow(dRf, (1 + 1.5 * (dRf - 0.1)))
            ms = math.pow((D / 20), 2) * 3.14 * L * 0.5
            Vd = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 1.5 / Rfmin
            Vsl = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 0.8
            Vw = ((1 - 0.5 / 2.5) * math.pow((D / 20), 2) * 3.14 * L) * 1.5 / Rfmin - Vsl

            n1 = Vw/10
            n2 = Vw/20 


            print("------------------------------------------------------------------\n")
            print(f"The recommended column has internal diameter D = {D:.0f}mm and length L = {L:.0f}cm")
            print(f"Mass of silica (g): ≈{ms:.0f}")

            print(" \n")

            print("Dry silica loading:")
            print(f"Volume of eluent for colomning (ml): {Vd:.0f}")

            print(" \n")

            print("Wet silica loading:")
            print(f"Volume of eluent for wet loading of silica (ml): {Vsl:.0f}")
            print(f"Volume of eluent for colomning (ml): {Vw:.0f}")

            print(" \n")

            print(f"Number of 10ml test tubes (small): {n1:.0f}")
            print(f"Number of 20ml test tubes (large): {n2:.0f}")

            again = input(
                "------------------------------------------------------------------\n"
                "\nDo you want to go to the main menu? \n"
                "1. Yes\n"
                "2. No\n"
                )

            if again == "1":
                continue

            if again == "2":  
                print("------------------------------------------------------------------\n"
                "QuickFC v.1.3, Flash Column Chromatography Calculator."
                "© 2024-2026 Dmitrii Ladan. All rights reserved. \n"
                "Goodbye!")
                break










    if choice1 == "3":
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
            print(f"V (pentane):  {pentane_result:.0f}")
            print(f"V (ethylacetate): {ea_result:.0f}")

            again = input(
                "\nDo you want to make calculations once again?\n"
                "1. Yes\n"
                "2. No\n"
                )

            if again == "1":
                continue

            if again == "2":
                print("------------------------------------------------------------------\n"
                "QuickFC v.1.3, Flash Column Chromatography Calculator."
                "© 2024-2026 Dmitrii Ladan. All rights reserved. \n"
                "Goodbye!")
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
                print("------------------------------------------------------------------\n"
                "QuickFC v.1.3, Flash Column Chromatography Calculator."
                "© 2024-2026 Dmitrii Ladan. All rights reserved. \n"
                "Goodbye!")
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
                    print("------------------------------------------------------------------\n"
                    "QuickFC v.1.3, Flash Column Chromatography Calculator."
                    "© 2024-2026 Dmitrii Ladan. All rights reserved. \n"
                    "Goodbye!")
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
                    print("------------------------------------------------------------------\n"
                    "QuickFC v.1.3, Flash Column Chromatography Calculator."
                    "© 2024-2026 Dmitrii Ladan. All rights reserved. \n"
                    "Goodbye!")
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
                print("------------------------------------------------------------------\n"
                "QuickFC v.1.3, Flash Column Chromatography Calculator."
                "© 2024-2026 Dmitrii Ladan. All rights reserved. \n"
                "Goodbye!")
                break