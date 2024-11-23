#Hier worden de lijst skills van de cv en vacature vergeleken, output is een percentage
class StringCompare:
    def calculate_match_percentage(cv_data, vacature_data):
        set1 = set(cv_data)
        set2 = set(vacature_data)

        common_elements = set1.intersection(set2)

        match_percentage = (len(common_elements) / len(set1)) * 100 if len(set1) > 0 else 0

        return match_percentage
        