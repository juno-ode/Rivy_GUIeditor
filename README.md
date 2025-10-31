# Rivy_GUIeditor
This is Rivy's GUI engine editor 

The Rivy Game Engine-editor Completion List
---
you can download the project manager if whanted go to the releases and click on one of them
---

| **Category**                     | **Done / Total** | **Completion %** |
| -------------------------------- | ---------------- | ---------------- |
| **ECS Setup**                    | 8 / 9            | **88.9%**        |
| **Entity Creation & Management** | 0 / 5            | 0%               |
| **Camera & Navigation**          | 1 / 6            | **16.7%**        |
| **File Explorer**                | 2 / 6            | **33.3%**        |
| **Scene Management**             | 0 / 3            | 0%               |
| **Asset Management**             | 0 / 6            | 0%               |
| **GUI & UI Systems**             | 0 / 6            | 0%               |
| **Editor Mode**                  | 0 / 5            | 0%               |
| **Rendering & Visualization**    | 1 / 6            | **16.7%**        |
| **Scripting & Automation**       | 0 / 4            | 0%               |
| **Tools & Utilities**            | 0 / 5            | 0%               |
| **Advanced Features**            | 0 / 3            | 0%               |


✅ Overall Progress: 12 / 58 → ~20.7% complete for realease


---
(` ~ `) means that it is done example ~added saying hi 
---
Editor Base Features

ECS Setup:

Integrate Bevy ECS for entity and component management.

Define components (e.g., Position, Velocity, Cube, Plane, Camera).

Implement systems to process components in the ECS world (e.g., physics, rendering, input systems).

~World Inspector

~Display list of entities in the current world.

Show entity IDs and names (with color coding based on entity type).

~Selectable entities for inspection.

~Display components attached to selected entities (e.g., Position, Cube, etc.).

~Show component details (e.g., type, value).

~Entity Creation & Management

Add entities to the world (with different components like Cube, Plane, Camera).

Remove entities from the world.

Modify entity components (e.g., change position, size, color).

Prefab system for reusing entities (e.g., save & load preset configurations).

~Camera & Navigation

~First-person camera using Raylib's camera system (WASD, mouse look).

Free movement and collision detection for camera.

Camera controls (e.g., zoom, rotate).

Entity selection via raycasting from camera to scene.

Camera modes: First person, third person, orthographic view.

File Explorer

~Browse project files (e.g., assets, scripts).

Open and edit files (e.g., scripts, shaders).

Create, delete, and rename files.

Preview files (e.g., textures, models).

~Navigation system for moving between directories.

File type filters (e.g., show only .txt, .shader, .model files).

Scene Management

Load and save scenes (ECS world states).

Import/export entities (e.g., to/from JSON or YAML).

Undo/redo functionality for scene editing.

Asset Management

Asset pipeline for textures, models, audio, etc.

Texture atlas generation for sprites.

3D model import (e.g., .obj, .fbx, .gltf).

Shader editor with live preview.

Audio system (load, play, and manipulate audio assets).

GUI & UI Systems

ImGui-based UI for editor interface.

Dockable windows for different editor panels (e.g., World Inspector, File Explorer, Scene).

Custom controls (e.g., sliders for properties, buttons for actions).

Live editing of component properties in the GUI.

UI layout system for flexibility (adjustable panels, resizable windows).

Editor Mode

Run-time debugging (inspect ECS entities during gameplay).

Pause/play modes for inspecting entities while the game is running.

Console log for error messages and debug output.

Real-time updates for component changes during runtime.

Rendering & Visualization

~Raylib integration for 3D rendering (cubes, planes, etc.).

Debug draw modes (e.g., draw bounding boxes, grid).

Entity gizmos (e.g., position handles, rotation/scale handles for entities).

Viewport controls (zoom, move, reset view).

Wireframe mode for visualizing the structure.

Scripting & Automation

Scripting support (e.g., Python, Lua) to control entities and behaviors.

Script editor with syntax highlighting, error checking.

Custom script binding for ECS components (e.g., attach scripts to entities).

Automation tools (e.g., macros, batch processes for entity manipulation).

Tools & Utilities

Profiler to track performance (FPS, memory usage).

Entity search (filter entities by name, type).

Undo/redo stack for editor actions.

Build & deployment system for game export.

Asset bundling for efficient packaging.

Advanced Features (Future Enhancements)

Multi-user editor for collaborative game development.

VR/AR support for immersive development environments.

Real-time network sync for multiplayer game testing.

This checklist outlines a comprehensive game engine editor based on Raylib and Bevy ECS, helping you organize tasks and keep track of features while developing!
