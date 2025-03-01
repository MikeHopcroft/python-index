import os
import sys
import tiktoken

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ts_type_filter import (
    Array,
    build_type_index,
    build_filtered_types,
    Define,
    Literal,
    ParamDef,
    ParamRef,
    Struct,
    Type,
    Union,
)

type_defs = [
    Define("Cart", [], Struct({"items": Array(Type("Item"))})),
    Define(
        "Item",
        [],
        Union(
            Type("WiseguyMeal", [ParamRef(Type("ComboSizes"))]),
            Type("Meal", [ParamRef(Type("ComboSizes"))]),
            Type("PattyMelt"),
            Type("Burger"),
            Type("Chicken"),
            Type("KoreanChicken"),
            Type(
                "GenericFountainDrink",
                [ParamRef(Type("DrinkNames")), ParamRef(Type("DrinkSizes"))],
            ),
        ),
    ),
    Define(
        "WiseguyMeal",
        [ParamDef("SIZE", Type("ComboSizes"))],
        Struct(
            {
                "name": Literal("Wiseguy Meal"),
                "size": Type("SIZE"),
                "sandwich": Union(Type("Wiseguy"), Type("CHOOSE")),
                "fries": Union(
                    Type("FrenchFries", [ParamRef(Type("SIZE"))]), Type("CHOOSE")
                ),
                "drink": Union(
                    Type(
                        "GenericFountainDrink",
                        [ParamRef(Type("DrinkNames")), ParamRef(Type("SIZE"))],
                    ),
                    Type("CHOOSE"),
                ),
            }
        ),
    ),
    Define(
        "Meal",
        [ParamDef("SIZE", Type("ComboSizes"))],
        Struct(
            {
                "name": Literal("Meal"),
                "size": Type("SIZE"),
                "sandwich": Union(
                    Type("Wiseguy"),
                    Type("PattyMelt"),
                    Type("Burger"),
                    Type("Chicken"),
                    Type("KoreanChicken"),
                    # Type("Pitas"),
                    # Type("Fish"),
                    # Type("CHOOSE"),
                ),
                "fries": Union(
                    Type("FrenchFries", [ParamRef(Type("SIZE"))]), Type("CHOOSE")
                ),
                "drink": Union(
                    Type(
                        "GenericFountainDrink",
                        [ParamRef(Type("DrinkNames")), ParamRef(Type("SIZE"))],
                    ),
                    Type("CHOOSE"),
                ),
            }
        ),
    ),
    Define(
        "Wiseguy",
        [],
        Type(
            "GenericWiseguy",
            [
                ParamRef(
                    Union(
                        Literal("Wiseguy"),
                        Literal("Vegan Wiseguy"),
                        Literal("Double Wiseguy"),
                        Literal("Triple Wiseguy"),
                        Literal("Down East Wiseguy"),
                    )
                )
            ],
        ),
    ),
    Define(
        "GenericWiseguy",
        [ParamDef("NAME")],
        Struct(
            {
                "name": Type("NAME"),
                "type": Union(
                    Literal("Regular", [], True),
                    Literal("With Bacon"),
                    Literal("With Cheese"),
                    Literal("With Bacon and Cheese"),
                    Type("CHOOSE"),
                ),
                "options?": Union(Type("Veggies"), Type("Sauces")),
            }
        ),
    ),
    Define(
        "PattyMelt",
        [],
        Struct(
            {
                "name": Union(
                    Literal("Hero Melt", ["patty"]),
                    Literal("Bacon Melt", ["patty"]),
                    Literal("Mushroom and Swiss Melt", ["patty"]),
                    Type("CHOOSE"),
                ),
                "options?": Array(
                    Union(
                        Type("Veggies"),
                        Type("Bacon"),
                        Type("Cheeses"),
                        Type("Sauces"),
                        Type("Condiments"),
                    )
                ),
            }
        ),
    ),
    Define(
        "Burger",
        [],
        Type(
            "GenericBurger",
            [
                ParamRef(
                    Union(
                        Literal("Bacon Double Cheeseburger"),
                        Literal("Bacon Cheeseburger"),
                        Literal("Double Cheeseburger"),
                        Literal("Cheeseburger"),
                    )
                )
            ],
        ),
    ),
    Define(
        "GenericBurger",
        [ParamDef("NAME")],
        Struct(
            {
                "name": Type("NAME"),
                "options?": Array(
                    Union(
                        Type("Veggies"),
                        Type("Bacon"),
                        Type("Cheeses"),
                        Type("Sauces"),
                        Type("Condiments"),
                        Type("Preparations"),
                        Type("Extras"),
                    )
                ),
            }
        ),
    ),
    Define(
        "Chicken",
        [],
        Type(
            "GenericChicken",
            [
                ParamRef(
                    Union(
                        Literal("Grilled Chicken Sandwich"),
                        Literal("Cordon Bleu", ["chicken sandwich blue"]),
                    )
                )
            ],
        ),
    ),
    Define(
        "GenericChicken",
        [ParamDef("NAME")],
        Struct(
            {
                "name": Type("NAME"),
                "options?": Array(
                    Union(
                        Type("Veggies"),
                        Type("Bacon"),
                        Type("GenericCheese", [ParamRef(Literal("American Cheese"))]),
                        Type("Condiments"),
                    )
                ),
            }
        ),
    ),
    Define(
        "KoreanChicken",
        [],
        Struct(
            {
                "name": Union(
                    Literal("Sweet and Spicy Chicken", ["Korean fried sandwich"]),
                    Literal("Seasame Soy Chicken", ["Korean fried sandwich"]),
                    Literal("Spicy Garlic Chicken", ["Korean fried sandwich"]),
                ),
                "options?": Array(
                    Union(
                        Type("Veggies"),
                        Type("Bacon"),
                        Type("Cheeses"),
                        Type("Sauces"),
                        Type("Condiments"),
                        Type("Preparations"),
                        Type("Extras"),
                    )
                ),
            }
        ),
    ),
    Define(
        "FrenchFries",
        [ParamDef("SIZE", Type("ComboSizes"))],
        Struct(
            {
                "name": Union(
                    Literal("French Fries"),
                    Literal("Onion Rings"),
                    Literal("Sweet Potato Fries"),
                ),
                "size": Type("SIZE"),
            }
        ),
    ),
    Define(
        "FrenchFrySize",
        [],
        Union(Literal("Value"), Literal("Small"), Literal("Medium"), Literal("Large")),
    ),
    Define(
        "GenericFrenchFries",
        [ParamDef("NAME"), ParamDef("SIZE", Type("FrenchFrySize"))],
        Struct(
            {
                "name": Type("NAME"),
                "size": Type("SIZE"),
            }
        ),
    ),
    Define(
        "OtherFries",
        [ParamDef("SIZE", Type("OtherFriesSizes"))],
        Struct(
            {
                "name": Union(
                    Literal("Jalopeno Poppers"),
                    Literal("Mozzarella Sticks"),
                ),
                "size": Type("SIZE"),
                "sauce": Type("DippingSauceFlavor"),
            }
        ),
    ),
    Define(
        "GenericOtherFries",
        [ParamDef("NAME"), ParamDef("SIZE", Type("OtherFriesSizes"))],
        Struct(
            {
                "name": Type("NAME"),
                "size": Type("SIZE"),
                "sauce": Type("DippingSauceFlavor"),
            }
        ),
    ),
    Define(
        "OtherFriesSizes",
        [],
        Union(Literal("4 Piece"), Literal("8 Piece"), Literal("12 Piece")),
    ),
    Define(
        "ComboSizes",
        [],
        Union(Literal("Small"), Literal("Medium"), Literal("Large"), Type("CHOOSE")),
    ),
    Define(
        "CHOOSE",
        [],
        Literal("CHOOSE", [], True),
        "Use CHOOSE when customer doesn't specify an option",
    ),
    Define(
        "GenericFountainDrink",
        [ParamDef("NAME", Type("DrinkNames")), ParamDef("SIZE", Type("DrinkSizes"))],
        Struct(
            {
                "name": Type("NAME"),
                "size": Type("SIZE"),
            }
        ),
    ),
    Define(
        "DrinkSizes",
        [],
        Union(
            Literal("Value"),
            Literal("Small"),
            Literal("Medium"),
            Literal("Large"),
            Type("CHOOSE"),
        ),
    ),
    Define(
        "DrinkNames",
        [],
        Union(
            Literal("Coca-Cola", ["coca", "cola", "coke"]),
            Literal("Diet Coke", ["coca", "cola"]),
            Literal("Coca-Cola Zero Sugar", ["coca", "cola", "coke"]),
            Literal("Dr. Pepper", ["doctor"]),
            Literal("Root Beer"),
            Literal("Diet Root Beer"),
            Literal("Sprite"),
            Literal("Sprite Zero"),
            Literal("Sweetened Tea"),
            Literal("Unsweetened Tea"),
            Literal("Strawberry Lemonade"),
            Literal("Arnold Palmer", ["iced team lemonade"]),
            Literal("Powerade Zero"),
        ),
    ),
    Define(
        "Veggies",
        [],
        Struct(
            {
                "amount": Type("ExtraAmount"),
                "name": Union(
                    Literal("Lettuce"),
                    Literal("Tomato"),
                    Literal("Onion"),
                    Literal("Pickles"),
                    Literal("Jalapeños"),
                ),
            }
        ),
    ),
    # Define(
    #     "Cheeses",
    #     [],
    #     Struct(
    #         {
    #             "amount": Type("Optional"),
    #             "name": Union(
    #                 Literal("American Cheese"),
    #                 Literal("Cheddar Cheese"),
    #                 Literal("Swiss Cheese"),
    #             ),
    #         }
    #     ),
    # ),
    # # TODO: make GenericCheese
    # Define(
    #     "AmericanCheese",
    #     [],
    #     Struct(
    #         {
    #             "amount": Type("Optional"),
    #             "name": Literal("American Cheese"),
    #         }
    #     ),
    # ),
    Define(
        "Cheeses",
        [],
        Type(
            "GenericCheese",
            [
                ParamRef(
                    Union(
                        Literal("American Cheese"),
                        Literal("Cheddar Cheese"),
                        Literal("Swiss Cheese"),
                    )
                )
            ],
        ),
    ),
    Define(
        "GenericCheese",
        [ParamDef("NAME")],
        Struct(
            {
                "name": Type("NAME"),
                "amount": Type("Optional"),
            }
        ),
    ),
    Define(
        "Bacon",
        [],
        Struct(
            {
                "amount": Type("Optional"),
                "name": Literal("Bacon"),
            }
        ),
    ),
    Define(
        "Condiments",
        [],
        Struct(
            {
                "amount": Type("Amount"),
                "name": Union(
                    Literal("Ketchup"),
                    Literal("Mustard"),
                    Literal("Mayo", ["mayonnaise", "hellmanns"]),
                    Literal("BBQ", ["barbecue"]),
                ),
            }
        ),
    ),
    Define(
        "Sauces",
        [],
        Struct(
            {
                "amount": Type("Amount"),
                "name": Union(
                    Literal("Smokey Sauce"),
                    Literal("Green Goddess Sauce"),
                ),
            }
        ),
    ),
    Define(
        "Extras",
        [],
        Struct(
            {
                "amount": Type("ExtraAmount"),
                "name": Union(Literal("Onion Rings"), Literal("Jalopenos")),
            }
        ),
    ),
    Define(
        "Preparations",
        [],
        Struct(
            {
                "amount": Type("Optional"),
                "name": Union(
                    Literal("Off Broiler"),
                    Literal("Cut in Half"),
                    Literal("Plain"),
                    Literal("Low Carb"),
                ),
            }
        ),
    ),
    Define(
        "Amounts",
        [],
        Union(Type("Amount"), Type("ExtraAmount"), Type("Optional")),
    ),
    Define(
        "Amount",
        [],
        Union(
            Literal("no"),
            Literal("light"),
            Literal("regular", [], True),
            Literal("extra"),
        ),
    ),
    Define(
        "ExtraAmount",
        [],
        Union(Literal("no"), Literal("regular", [], True), Literal("extra")),
    ),
    Define(
        "Optional",
        [],
        Union(Literal("no"), Literal("regular", [], True)),
    ),
]


def format_menu(type_defs):
    return "\n".join([x.format() for x in type_defs])


def go():
    encoder = tiktoken.get_encoding("cl100k_base")

    if len(sys.argv) <= 1:
        print("Using default query because no query was specified on the command line.")
    default_query = "mushroom melt with extra mayo and no tomatoes"
    query = sys.argv[1] if len(sys.argv) > 1 else default_query

    #
    # Print out original type definition
    #
    original = format_menu(type_defs)
    original_tokens = len(encoder.encode(original))
    print(original)

    #
    # Print out filtered type definition
    #
    print("=== Filtered Types =====================")

    symbols, indexer = build_type_index(type_defs)
    reachable = build_filtered_types(type_defs, symbols, indexer, query)

    for n in reachable:
        print(n.format())

    print()
    print("!!! Pruned Types!!!!!!!!!!!!!!!!")
    pruned = format_menu(reachable)
    pruned_tokens = len(encoder.encode(pruned))
    print(pruned)

    print()
    print(f"query: {query}")
    print(f"tokens (original): {original_tokens}")
    print(f"tokens (pruned): {pruned_tokens}")
    pruned_percentage = (pruned_tokens / original_tokens) * 100
    print(f"percentage pruned: {pruned_percentage:.2f}%")


if __name__ == "__main__":
    go()
