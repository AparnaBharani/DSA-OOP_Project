import folium
import webbrowser
import os

class CampusMap:
    def __init__(self, campus_location, zoom_start=17):
        """Initialize the campus map with a given location and zoom level."""
        self.campus_location = campus_location
        self.map = folium.Map(location=self.campus_location, zoom_start=zoom_start)

    def add_building(self, name, latitude, longitude, info):
        """Add a building marker to the campus map."""
        folium.Marker(
            location=[latitude, longitude],
            popup=f"<b>{name}</b><br>{info}",
            tooltip=name,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(self.map)

    def save_map(self, filename="campus_map.html"):
        """Save the map to an HTML file."""
        self.map.save(filename)
        print(f"Map has been saved as '{filename}'.")
        file_path = os.path.abspath(filename)
        webbrowser.open(f"file://{file_path}")

# Campus location
campus_location = [10.9027, 76.9006]

# Create an instance of CampusMap
amrita_map = CampusMap(campus_location)

# Dictionary of buildings
buildings = {
    "Library": [10.904269877578768, 76.89916340902396, "Contains 50,000+ books, journals"],
    "Main Canteen": [10.900176154247136, 76.9038455462262, "Serves Non-Veg food"],
    "Amrita School of Business": [10.904367435871444, 76.90187231916259, "MBA (Master of Business Administration) - General,MBA in Business Analytics,MBA in Finance,MBA in Human Resources,MBA in Marketing,MBA in Operations Management"],
    "Academic Block 1": [10.900454111970278, 76.90289195209053,
                         "Departments: Aerospace, Mechanical, M.Sc Data Science, M.Sc Physics, M.Sc Chemistry, Non-Academic: Administration Office"],
    "Academic Block 2": [10.904150503475744, 76.89856865920655, "Departments: ECE, ELC, EEE, CCE"],
    "Academic Block 3": [10.90642608218763, 76.8976996235012, "Departments: CSE, CSE(CYS),CSE(AI)"],
    "Kapila Bhavanam": [10.904473107380893, 76.90062548352138, "Boys Hostel"],
    "Amriteshwari Hall": [10.900555795290602, 76.90373360432955,"Event Hall"],
    "Dhanalakshmi Bank":[10.899617279027856, 76.90036324660845,"Bank"],
    "Mythereyi Bhavanam":[10.90056945062219, 76.90127043803365,"Girls Hostel"],
    "General Store":[10.901753134837179, 76.9018214243655,"Clinic,Naturals SPA N salon,General store,SBI Bank"],
    "Amrita Ashram":[10.902106837581025, 76.9010597720397,"Place to Meditate"],
    "Gargi Bhavanam":[10.90294767686437, 76.89967134227187,"PG Girls Hostel"],
    "Aditi Bhavanam":[10.907440389812052, 76.89927954240942,"Girls Hostel"],
    "IT Canteen":[10.904938311755762, 76.89811077764885,"Serves Non-Veg food"],
    "Kashyapa bhavanam":[10.903075025582275, 76.90556517563276,"Boys Hostel"],
    "CIR":[10.905412896318309, 76.90196731312494,"Corporate & Industry Relations"],
    "Agasthya Bhavanam":[10.90265283739445, 76.89625027778469,"Boys Hostel"],
    "Vasishita Bhavanam":[10.901732004499594, 76.89605054391042,"Boys Hostel"],
    "Yagnavalkya Bhavanam" :[10.901473695072792, 76.90482149437298,"Boys Hostel"],
    "Nachiketas Bhavanam":[10.900621242349255, 76.90481511115499,"Boys Hostel"],
    "Central Kitchen":[10.901448705669322, 76.90120216719838,"Mess Food Making Place"],
    "MBA Canteen":[10.904614027562427, 76.90225596379726,"Serves Veg Food"],
    "VB Mess":[10.903017104810402, 76.89621068532482,"VB Mess Hall"],
    "Indoor Badminton Court an Boys GYM":[10.90152637492918, 76.89483739430992,"Badminton Court"],
    "Automotive Research and Testing Centre":[10.903845226504012, 76.89567815296341,"Research Lab"],
    "Swimming Pool":[10.90602715392933, 76.8988539359285],
    "Millet Cafe":[10.90698713371892, 76.89906238290862,"Serves Tiffin"],
    "Department of Mass Communication":[10.905051139921744, 76.89909465654178],
    "Amritanjali Hall":[10.904751064131462, 76.8992096047763,"Lecture Hall"],
    "Guest House":[10.90152511492906, 76.89892106424408],
    "Gauthama Bhavanam":[10.9025709655824, 76.89732649966285,"Boys Hostel"],
    "Auditorium":[10.904675418849024, 76.90264911711347,"Events and Programs"],
    "Ground":[10.902662705407488, 76.90324441467796],
    "Yagnavalkya Bhavanam Annexe":[10.902926785055959, 76.90507280659004,"Boys Hostel"],
    "Vyasa Maharishi Bhavanam":[10.901481382106102, 76.9053984241848,"Boys Hostel"],
    "Boys GYM":[10.90191251592289, 76.90211156053164]
}

# Add buildings to the map using the OOP approach
for name, values in buildings.items():
    if len(values) == 3:
        lat, lon, info = values
    else:
        lat, lon = values
        info = "No description available."
    amrita_map.add_building(name, lat, lon, info)


# Save the final map
amrita_map.save_map()

print("Map updated with clickable buildings! Open 'campus_map.html' to view.")