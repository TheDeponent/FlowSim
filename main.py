
from app.__GUI import demo

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch FlowSim Gradio app")
    parser.add_argument('--public', action='store_true', help='Launch on a public Gradio link (share=True)')
    args = parser.parse_args()
    demo.launch(server_name="0.0.0.0", share=True)
