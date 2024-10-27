# beam_library.py

import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Material:
    name: str
    E: float  # Modulus of Elasticity in Pascals


@dataclass
class Beam:
    name: str
    length: float  # Length of the beam in meters
    width: float  # Width of the beam in meters
    thickness: float  # Thickness of the beam in meters

    def moment_of_inertia(self) -> float:
        """Calculate the Moment of Inertia for a rectangular cross-section."""
        return (self.width * self.thickness ** 3) / 12


@dataclass
class Load:
    name: str
    w: float  # Distributed load in N/m


class BeamLibrary:
    def __init__(self, filepath: str = "library_data.json"):
        self.filepath = filepath
        self.materials: List[Material] = []
        self.beams: List[Beam] = []
        self.loads: List[Load] = []
        self.load_library()

    def load_library(self):
        """Load library data from a JSON file."""
        if not os.path.exists(self.filepath):
            self.initialize_default_library()
            self.save_library()
        else:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                self.materials = [Material(**mat) for mat in data.get("materials", [])]
                self.beams = [Beam(**beam) for beam in data.get("beams", [])]
                self.loads = [Load(**load) for load in data.get("loads", [])]

    def save_library(self):
        """Save library data to a JSON file."""
        data = {
            "materials": [asdict(mat) for mat in self.materials],
            "beams": [asdict(beam) for beam in self.beams],
            "loads": [asdict(load) for load in self.loads]
        }
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Library data saved to '{self.filepath}'.")

    def initialize_default_library(self):
        """Initialize the library with default materials, beams, and loads."""
        # Define default Materials
        default_materials = [
            Material(name="Steel", E=200e9),
            Material(name="Aluminum", E=69e9),
            Material(name="Titanium", E=116e9)
        ]
        self.materials.extend(default_materials)

        # Define default Beams
        default_beams = [
            Beam(name="Beam1", length=10.0, width=0.3, thickness=0.005),
            Beam(name="Beam2", length=8.0, width=0.25, thickness=0.004)
        ]
        self.beams.extend(default_beams)

        # Define default Loads
        default_loads = [
            Load(name="Uniform Load", w=1000.0),  # 1000 N/m
            Load(name="Heavy Uniform Load", w=2000.0)  # 2000 N/m
        ]
        self.loads.extend(default_loads)

    def add_material(self, material: Material):
        """Add a new material to the library."""
        if any(mat.name.lower() == material.name.lower() for mat in self.materials):
            print(f"Material '{material.name}' already exists.")
            return
        self.materials.append(material)
        print(f"Material '{material.name}' added.")

    def add_beam(self, beam: Beam):
        """Add a new beam to the library."""
        if any(b.name.lower() == beam.name.lower() for b in self.beams):
            print(f"Beam '{beam.name}' already exists.")
            return
        self.beams.append(beam)
        print(f"Beam '{beam.name}' added.")

    def add_load(self, load: Load):
        """Add a new load to the library."""
        if any(ld.name.lower() == load.name.lower() for ld in self.loads):
            print(f"Load '{load.name}' already exists.")
            return
        self.loads.append(load)
        print(f"Load '{load.name}' added.")

    def remove_material(self, material_name: str):
        """Remove a material from the library."""
        material = next((mat for mat in self.materials if mat.name.lower() == material_name.lower()), None)
        if not material:
            print(f"Material '{material_name}' not found.")
            return
        # Optional: Check if any beam or load is using this material
        # For now, assume materials are independent
        self.materials.remove(material)
        print(f"Material '{material_name}' removed.")

    def remove_beam(self, beam_name: str):
        """Remove a beam from the library."""
        beam = next((b for b in self.beams if b.name.lower() == beam_name.lower()), None)
        if not beam:
            print(f"Beam '{beam_name}' not found.")
            return
        self.beams.remove(beam)
        print(f"Beam '{beam_name}' removed.")

    def remove_load(self, load_name: str):
        """Remove a load from the library."""
        load = next((ld for ld in self.loads if ld.name.lower() == load_name.lower()), None)
        if not load:
            print(f"Load '{load_name}' not found.")
            return
        self.loads.remove(load)
        print(f"Load '{load_name}' removed.")

    def get_materials(self) -> List[Material]:
        return self.materials

    def get_beams(self) -> List[Beam]:
        return self.beams

    def get_loads(self) -> List[Load]:
        return self.loads

    def modify_beam_dimensions(self, beam_name: str, new_length: Optional[float] = None,
                               new_width: Optional[float] = None, new_thickness: Optional[float] = None):
        """Modify the dimensions of an existing beam."""
        beam = next((b for b in self.beams if b.name.lower() == beam_name.lower()), None)
        if not beam:
            print(f"Beam '{beam_name}' not found.")
            return
        if new_length is not None:
            beam.length = new_length
            print(f"Beam '{beam_name}' length updated to {new_length} m.")
        if new_width is not None:
            beam.width = new_width
            print(f"Beam '{beam_name}' width updated to {new_width} m.")
        if new_thickness is not None:
            beam.thickness = new_thickness
            print(f"Beam '{beam_name}' thickness updated to {new_thickness} m.")

    def view_library(self):
        """Display current materials, beams, and loads."""
        print("\n--- Materials ---")
        if not self.materials:
            print("No materials available.")
        else:
            for mat in self.materials:
                print(f"Name: {mat.name}, E: {mat.E} Pa")

        print("\n--- Beams ---")
        if not self.beams:
            print("No beams available.")
        else:
            for beam in self.beams:
                print(
                    f"Name: {beam.name}, Length: {beam.length} m, Width: {beam.width} m, Thickness: {beam.thickness} m, I: {beam.moment_of_inertia():.6e} m^4")

        print("\n--- Loads ---")
        if not self.loads:
            print("No loads available.")
        else:
            for load in self.loads:
                print(f"Name: {load.name}, w: {load.w} N/m")
        print()


def add_new_material(library: BeamLibrary):
    print("\nAdd New Material")
    name = input("Enter material name: ").strip()
    if not name:
        print("Material name cannot be empty.")
        return
    try:
        E_input = input("Enter Modulus of Elasticity E [Pa]: ").strip()
        E = float(E_input)
        if E <= 0:
            print("Modulus of Elasticity must be positive.")
            return
    except ValueError:
        print("Invalid input for E. Must be a number.")
        return
    material = Material(name=name, E=E)
    library.add_material(material)


def add_new_beam(library: BeamLibrary):
    print("\nAdd New Beam")
    name = input("Enter beam name: ").strip()
    if not name:
        print("Beam name cannot be empty.")
        return
    try:
        length_input = input("Enter beam length [m]: ").strip()
        length = float(length_input)
        if length <= 0:
            print("Beam length must be positive.")
            return
        width_input = input("Enter beam width [m]: ").strip()
        width = float(width_input)
        if width <= 0:
            print("Beam width must be positive.")
            return
        thickness_input = input("Enter beam thickness [m]: ").strip()
        thickness = float(thickness_input)
        if thickness <= 0:
            print("Beam thickness must be positive.")
            return
    except ValueError:
        print("Invalid input for dimensions. Must be numbers.")
        return
    beam = Beam(name=name, length=length, width=width, thickness=thickness)
    library.add_beam(beam)


def add_new_load(library: BeamLibrary):
    print("\nAdd New Load")
    name = input("Enter load name: ").strip()
    if not name:
        print("Load name cannot be empty.")
        return
    try:
        w_input = input("Enter distributed load w [N/m]: ").strip()
        w = float(w_input)
    except ValueError:
        print("Invalid input for w. Must be a number.")
        return
    load = Load(name=name, w=w)
    library.add_load(load)


def modify_existing_beam(library: BeamLibrary):
    print("\nModify Existing Beam Dimensions")
    beam_name = input("Enter the name of the beam to modify: ").strip()
    if not beam_name:
        print("Beam name cannot be empty.")
        return
    beam = next((b for b in library.get_beams() if b.name.lower() == beam_name.lower()), None)
    if not beam:
        print(f"Beam '{beam_name}' not found.")
        return
    print(
        f"Current dimensions of '{beam.name}': Length={beam.length} m, Width={beam.width} m, Thickness={beam.thickness} m")
    try:
        new_length_input = input("Enter new length [m] (press Enter to keep current): ").strip()
        new_length = float(new_length_input) if new_length_input else None
        new_width_input = input("Enter new width [m] (press Enter to keep current): ").strip()
        new_width = float(new_width_input) if new_width_input else None
        new_thickness_input = input("Enter new thickness [m] (press Enter to keep current): ").strip()
        new_thickness = float(new_thickness_input) if new_thickness_input else None
    except ValueError:
        print("Invalid input for dimensions. Must be numbers.")
        return
    library.modify_beam_dimensions(beam_name, new_length, new_width, new_thickness)


def remove_element(library: BeamLibrary):
    """Remove elements from the library: Materials, Beams, or Loads."""
    while True:
        print("\n--- Remove Elements ---")
        print("1. Remove Material")
        print("2. Remove Beam")
        print("3. Remove Load")
        print("4. Back to Main Menu")
        choice = input("Select an option (1-4): ").strip()

        if choice == '1':
            # Remove Material
            if not library.get_materials():
                print("No materials available to remove.")
                continue
            print("\nAvailable Materials:")
            for mat in library.get_materials():
                print(f"- {mat.name}")
            mat_name = input("Enter the name of the material to remove: ").strip()
            if not mat_name:
                print("Material name cannot be empty.")
                continue
            confirm = input(f"Are you sure you want to remove material '{mat_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                library.remove_material(mat_name)
            else:
                print("Removal canceled.")

        elif choice == '2':
            # Remove Beam
            if not library.get_beams():
                print("No beams available to remove.")
                continue
            print("\nAvailable Beams:")
            for beam in library.get_beams():
                print(f"- {beam.name}")
            beam_name = input("Enter the name of the beam to remove: ").strip()
            if not beam_name:
                print("Beam name cannot be empty.")
                continue
            confirm = input(f"Are you sure you want to remove beam '{beam_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                library.remove_beam(beam_name)
            else:
                print("Removal canceled.")

        elif choice == '3':
            # Remove Load
            if not library.get_loads():
                print("No loads available to remove.")
                continue
            print("\nAvailable Loads:")
            for load in library.get_loads():
                print(f"- {load.name}")
            load_name = input("Enter the name of the load to remove: ").strip()
            if not load_name:
                print("Load name cannot be empty.")
                continue
            confirm = input(f"Are you sure you want to remove load '{load_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                library.remove_load(load_name)
            else:
                print("Removal canceled.")

        elif choice == '4':
            # Back to Main Menu
            break
        else:
            print("Invalid option. Please select a number between 1 and 4.")


def main():
    library = BeamLibrary()

    while True:
        print("\n=== Beam Library Management ===")
        print("1. View Current Library")
        print("2. Add New Material")
        print("3. Add New Beam")
        print("4. Add New Load")
        print("5. Modify Existing Beam Dimensions")
        print("6. Remove Elements")
        print("7. Save and Exit")
        print("8. Exit without Saving")
        choice = input("Select an option (1-8): ").strip()

        if choice == '1':
            library.view_library()
        elif choice == '2':
            add_new_material(library)
        elif choice == '3':
            add_new_beam(library)
        elif choice == '4':
            add_new_load(library)
        elif choice == '5':
            modify_existing_beam(library)
        elif choice == '6':
            remove_element(library)
        elif choice == '7':
            library.save_library()
            print("Exiting and saving changes.")
            break
        elif choice == '8':
            confirm = input("Are you sure you want to exit without saving? (y/n): ").strip().lower()
            if confirm == 'y':
                print("Exiting without saving.")
                break
            else:
                print("Exit canceled.")
        else:
            print("Invalid option. Please select a number between 1 and 8.")


if __name__ == "__main__":
    main()
