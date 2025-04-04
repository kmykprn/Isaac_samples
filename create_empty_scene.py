import argparse
from isaaclab.app import AppLauncher

# ステップ0. 引数を受け取る
parser = argparse.ArgumentParser(description="Tutorial on creating an empty stage.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# ステップ1. シミュレータの起動
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# ステップ2. Isaac Sim（や他のライブラリ）からモジュールをインポート
from isaaclab.sim import SimulationCfg, SimulationContext

# ステップ3. シミュレーションコンテキストの設定
sim_cfg = SimulationCfg(dt=0.01)
sim = SimulationContext(sim_cfg)

# ステップ4. ビューポートを映すカメラの位置・注視点を設定
sim.set_camera_view([2.5, 2.5, 2.5], [0.0, 0.0, 0.0])

# ステップ5. シミュレーションの実行
sim.reset()
while simulation_app.is_running():
    sim.step()

# ステップ6. シミュレーションを終了
simulation_app.close()