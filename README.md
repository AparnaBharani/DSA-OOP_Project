Project Title:

Digital Twin of Amrita Vishwa Vidyapeetham Coimbatore Campus


Guided By:

Prajisha C. Assistant Professor, Amrita School of Artificial Intelligence, Coimbatore

Dr. Abhijith A Assistant Professor, Amrita School of Artificial Intelligence, Coimbatore



Team Members:

Aparna Bharani(CB.SC.U4AIE24304)

I.Mahalakshmi(CB.SC.U4AIE24322)

Maalika.P(CB.SC.U4AIE24332)

Parkavi.R(CB.SC.U4AIE24338)


Project Overview:

This project creates an interactive digital twin of the university campus using OpenStreetMap (OSM) and Python. It enhances campus navigation and accessibility through:


Clickable Buildings – Users can select buildings to view department details.

Shortest Path Navigation – Implemented using Dijkstra’s Algorithm to find the fastest route between two blocks.

Canteen Menu Updates – Dynamic system to fetch and update daily menus.



Technologies Used:

Programming Language: Python

Libraries: NetworkX, Flask, OpenStreetMap API

Database: JSON (future integration with SQLite)

Frontend: HTML, JavaScript (for OpenStreetMap integration)



System Architecture:

The project follows a modular design, separating data handling, pathfinding, and user interaction.

CampusMap Class – Manages buildings and paths.

Graph Class – Represents the campus as a weighted graph.

DijkstraAlgorithm Class – Implements shortest pathfinding.

DatabaseManager Class – Manages canteen menu updates.

View Campus Map – The home page loads an interactive OpenStreetMap with clickable buildings.

Find Shortest Path – Enter start and destination buildings to compute the fastest route.

Check Canteen Menu – Click on the canteen to see the latest menu updates.



Future Enhancements:

3D Visualization with Mapbox GL JS.

Mobile App Integration for real-time navigation.

IoT-based Live Updates on facility availability.

AI-powered Route Optimization for better path suggestions.
