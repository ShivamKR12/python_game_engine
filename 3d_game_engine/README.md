# 3D Game Engine

This is a 3D game engine built using Python, Pygame, and PyOpenGL. It features a basic physics engine, rendering, and input handling.

## Project Structure

project_root/
│
├── assets/
│ ├── models/
│ │ └── block.mtl
│ │ └── block.obj
│ │ └──grass_block.png
│ └── texture/
│
├── shaders/
│ ├── vertex_shader.glsl
│ └── fragment_shader.glsl
│
├── src/
│ ├── init.py
│ ├── game_engine.py
│ ├── input_handler.py
│ ├── main.py
│ ├── physics.py
│ ├── renderer.py
│ └── utils.py
│
├── README.md
└── requirements.txt


## Installation

1. Clone the repository:
    ```
    git clone https://github.com/your_username/3d_game_engine.git
    cd 3d_game_engine
    ```

2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Run the game engine:
    ```
    python src/main.py
    ```

## Dependencies

- Python 3.x
- Pygame
- PyOpenGL
- Pyrr

## License

This project is licensed under the MIT License.
