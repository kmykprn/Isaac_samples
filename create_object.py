import argparse
from isaaclab.app import AppLauncher


# ステップ0. 引数を受け取る
parser = argparse.ArgumentParser(description="Tutorial on spawning prims into the scene.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# ステップ1. シミュレータの起動
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# ステップ2. Isaac Simからモジュールをインポート
import isaaclab.sim as sim_utils


def create_scene():
    """
    空のシーン内に地面、ライト、直方体を配置する
    """

    # 地面を配置
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/defaultGroundPlane", cfg_ground)

    # ライトを配置
    cfg_light_distant = sim_utils.DistantLightCfg(
        intensity=3000.0,
        color=(0.75, 0.75, 0.75),
    )
    cfg_light_distant.func("/World/lightDistant", cfg_light_distant, translation=(1, 0, 10))

    # Rigid Bodyを付与していない（=視覚的な）直方体を配置
    cfg_cuboid_visual = sim_utils.CuboidCfg(
        size=(0.5, 0.5, 0.5),
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 0.0, 1.0)),
    )
    cfg_cuboid_visual.func("/World/Objects/CuboidDeformable_visual", cfg_cuboid_visual, translation=(0.0, -0.5, 1.5))

    # Rigid Bodyを付与した直方体を配置
    cfg_cuboid_physics = sim_utils.CuboidCfg(
        size=(0.5, 0.5, 0.5),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(rigid_body_enabled=True),
        mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
        collision_props=sim_utils.CollisionPropertiesCfg(),
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0)),
    )
    cfg_cuboid_physics.func("/World/Objects/CuboidDeformable_physics", cfg_cuboid_physics, translation=(0.0, 0.5, 1.5))


# ステップ3. シミュレーションコンテキストの設定
sim_cfg = sim_utils.SimulationCfg(dt=0.01, device=args_cli.device)
sim = sim_utils.SimulationContext(sim_cfg)

# ステップ4. ビューポートを映すカメラの位置・注視点を設定
sim.set_camera_view([3.0, 0.0, 2.5], [-0.5, 0.0, 0.5])

# ステップ5. 地面、ライト、直方体をシーンに配置
create_scene()

# ステップ6. シミュレーションの実行
sim.reset()
while simulation_app.is_running():
    sim.step()

# ステップ7. シミュレーションを終了
simulation_app.close()