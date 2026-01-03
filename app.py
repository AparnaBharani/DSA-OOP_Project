from flask import Flask, render_template, request, redirect, url_for, send_file, session
import folium
import osmnx as ox
import networkx as nx
import os
import json
from geopy.distance import geodesic
from datetime import datetime

app = Flask(__name__)
app.secret_key = "campusmapsecretkey"  # required for admin login session

campus_location = [10.9027, 76.9006]

# ==== Buildings Dictionary ====
buildings = {
    "Library": [10.904269877578768, 76.89916340902396, "50,000+ books & journals"],
    "Main Canteen": [10.900176154247136, 76.9038455462262, "Delicious meals"],
     "Amrita School of Business": [10.904367435871444, 76.90187231916259, "MBA Programs"],
    "Academic Block 1": [10.900454111970278, 76.90289195209053, "Departments: Aerospace, Mechanical, Data Science"],
    "Academic Block 2": [10.904150503475744, 76.89856865920655, "Departments: ECE, EEE, CCE"],
    "Academic Block 3": [10.90642608218763, 76.8976996235012, "Departments: CSE, AI, Cybersecurity"],
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

# ==== Canteen Menu Loader ====
class CanteenMenu:
    def __init__(self, filepath="menu.json"):
        self.filepath = filepath

    def get_today_menu(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
            today = datetime.now().strftime("%Y-%m-%d")
            return data if data.get("date") == today else {}
        except:
            return {}

# ==== Graph Class ====
class CampusGraph:
    def __init__(self, network_type='walk'):
        print("📦 Fetching OSM data...")
        self.graph = ox.graph_from_point(campus_location, dist=1000, network_type=network_type)
        print("✅ Graph created with", len(self.graph.nodes), "nodes")

    def get_nearest_node(self, coords):
        lat, lon = coords
        try:
            return ox.distance.nearest_nodes(self.graph, lon, lat)
        except Exception as e:
            print("⚠️ Node error:", e)
            return None

    def find_shortest_path(self, start_coords, end_coords):
        start_node = self.get_nearest_node(start_coords)
        end_node = self.get_nearest_node(end_coords)

        if not start_node or not end_node:
            return None, 0

        try:
            # Get all shortest paths with the same total distance
            paths = list(nx.all_shortest_paths(self.graph, source=start_node, target=end_node, weight='length'))

            # Tie-breaker: pick lex smallest path
            path = min(paths)
            total_distance = 0
            print("\n🔍 Route (node IDs):")
            for node in path:
                print(f"{node}", end=" → ")
            print("END")

            for u, v in zip(path[:-1], path[1:]):
                edge_length = self.graph[u][v][0].get('length', 0)
                total_distance += edge_length

            return path, total_distance / 1000
        except nx.NetworkXNoPath:
            print("❌ No path found.")
            distance = geodesic(start_coords, end_coords).km
            if distance < 0.3:
                print(f"⚠ Fallback path: {distance:.2f} km")
                return [start_coords, end_coords], distance
            return None, 0

# ==== Folium Map Renderer ====
class CampusMapRenderer:
    def __init__(self, location, zoom=17):
        self.map = folium.Map(location=location, zoom_start=zoom)

    def add_building_markers(self, building_dict):
        for name, (lat, lon, *desc) in building_dict.items():
            popup_text = f"<b>{name}</b><br>{desc[0]}" if desc else name
            folium.Marker(
                location=[lat, lon],
                popup=popup_text,
                tooltip=name,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(self.map)

    def draw_path(self, graph, path, start_coords, end_coords, distance):
        if path:
            if isinstance(path[0], (list, tuple)):
                folium.PolyLine(path, color="orange", weight=4, dash_array='5').add_to(self.map)
            else:
                route = [(graph.graph.nodes[n]['y'], graph.graph.nodes[n]['x']) for n in path]
                folium.PolyLine(route, color="red", weight=5).add_to(self.map)

            folium.Marker(start_coords, icon=folium.Icon(color="green"), popup="Start").add_to(self.map)
            folium.Marker(end_coords, icon=folium.Icon(color="red"), popup=f"End - {distance:.2f} km").add_to(self.map)

    def save(self, filename="static/campus_map.html"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.map.save(filename)

# ==== Instances ====
campus_graph = CampusGraph()
canteen_menu = CanteenMenu()

# ==== Routes ====

@app.route('/')
def index():
    menu = canteen_menu.get_today_menu()
    notifications=[
         "Guest Lecture at 2 PM in Amriteshwari Hall",
        "Library will close by 5:00 PM today!",
        "Join the Yoga Session near the Ashram at 6 AM"
    ]

    return render_template("index.html", buildings=buildings, menu=menu, notifications=notifications)

@app.route('/find_path', methods=['POST'])
def find_path():
    start = request.form.get("start")
    end = request.form.get("end")

    if start not in buildings or end not in buildings:
        return "Invalid building selection", 400

    start_coords = buildings[start][:2]
    end_coords = buildings[end][:2]
    path, distance = campus_graph.find_shortest_path(start_coords, end_coords)

    renderer = CampusMapRenderer(campus_location)
    renderer.add_building_markers(buildings)
    renderer.draw_path(campus_graph, path, start_coords, end_coords, distance)
    renderer.save()

    return redirect(url_for("show_map", distance=round(distance, 2)))

@app.route('/map')
def show_map():
    distance = request.args.get("distance")
    try:
        distance = float(distance)
    except:
        distance = None
    return render_template("map_view.html", distance=distance)

@app.route('/view')
def view_map_file():
    return send_file("static/campus_map.html")

# ==== Admin Login ====
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "admin@amrita.edu" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for('admin_menu'))
        else:
            return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")

@app.route('/admin/logout')
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for('index'))

# ==== Admin Menu Upload (Login Required) ====
@app.route('/admin/menu', methods=['GET', 'POST'])
def admin_menu():
    if not session.get("admin_logged_in"):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        date = datetime.now().strftime('%Y-%m-%d')
        main = request.form.getlist('main[]')
        mba = request.form.getlist('mba[]')
        it = request.form.getlist('it[]')

        new_menu = {
            "date": date,
            "Main Canteen": [i.strip() for i in main if i.strip()],
            "MBA Canteen": [i.strip() for i in mba if i.strip()],
            "IT Canteen": [i.strip() for i in it if i.strip()]
        }

        with open("menu.json", "w") as f:
            json.dump(new_menu, f, indent=2)

        return redirect(url_for('index'))

    return render_template("admin_menu.html")

# ==== Run App ====
if __name__ == '__main__':
    app.run(debug=True)
