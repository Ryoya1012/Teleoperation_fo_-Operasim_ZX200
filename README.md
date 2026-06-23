# Teleoperation of the zx200 compatible with Opera-sim(AGX version)

# 概要
- このリポジトリは, Opera-sim(AGX版)で実装されているドラグショベル(zx200)をコントローラ(Dual Sense / ELECOM Gaming Controller)で操作するためのノードである.

## 依存パッケージ
- [ps_ros2_common](https://github.com/Ar-Ray-code/ps_ros2_common/)


## 仕様
- 使用については, 以下の依存パッケージとシミュレーション環境が用意されていれば使用することができる.
- コントローラ(左右のジョイステック)のアサインは図1の通りであり新JIS規格に習っている.

<img width="2094" height="1480" alt="Controller operation lever assignment" src="https://github.com/user-attachments/assets/d0e438b2-90d6-424e-b928-20795a32a6c7" />


## ビルド・実行方法
```bash
cd ~/ros2_ws/src
```

```bash
git clone https://github.com/Ryoya1012/Teleoperation_for_Operasim_ZX200.git
```
※ branchがagx_versionに居るかの確認をすること

```bash
git clone https://github.com/Ar-Ray-code/ps_ros2_common.git
```

```bash
ros2 run joy joy_node
# 別ウィンドウで以下を実行
ros2 run my_teleop zx200_teleop_node
```
