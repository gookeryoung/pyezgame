# Sprite Assets

游戏精灵图资源列表，所有文件为 24-bit RGB PNG 格式，使用品红色 `0xFF00FF` (R=255, G=0, B=255) 作为透明色键。
保存在 `assets/` 文件夹内。

## 独立精灵 (Single Sprites)

单张图片的精灵资源，可直接用于游戏对象。

| 文件名 | 图片大小 | 说明 |
|--------|----------|------|
| player_ship.png | 32x32 | 玩家飞船，俯视视角朝上的太空飞船，青色机身、蓝色座舱、灰色机翼、橙黄色引擎尾焰 |
| enemy_ship.png | 32x32 | 敌方飞船，俯视视角朝下的外星飞船，红色倒三角机身、黄色驾驶舱（眼睛造型）、暗色侧翼 |
| bullet.png | 32x32 | 子弹/发射物，垂直方向的黄色光弹，顶部圆润、底部带橙色拖尾 |
| character.png | 32x48 | RPG 风格角色，像素小人，棕色头发、肤色面部、蓝色上衣、腰带、棕色裤子和靴子 |
| coin.png | 32x32 | 金币，圆形金色硬币，带内环浮雕和 `$` 符号，左上角高光 |
| heart.png | 32x32 | 爱心，红色心形图案，带粉色高光和暗红色阴影，适合表示生命值/血量 |
| fruit_apple.png | 32x32 | 苹果，红色苹果，带棕色果柄和绿色叶子，有明暗光影效果 |
| star.png | 32x32 | 五角星，黄色五角星形状，左上侧亮色、右下侧暗色，中心高亮，适合表示收集物/评分 |
| gem.png | 32x32 | 宝石/钻石，青绿色菱形宝石，上半部分亮色切面、下半部分暗色切面，带闪光点 |
| tree.png | 32x64 | 树木，三层绿色圆形树冠（由小到大），棕色树干，带明暗层次，适合场景装饰 |
| plane0.png | 32x32 | 红色飞机，从 demonstar.png 提取的红色飞机精灵帧 |
| plane1.png | 32x32 | 蓝色飞机，从 demonstar.png 提取的蓝色飞机精灵帧 |

## 精灵表 (Sprite Sheets)

包含多帧动画的精灵表，按水平方向排列各帧。

| 文件名 | 图片大小 | 帧大小 | 帧数 | 说明 |
|--------|----------|--------|------|------|
| explosion.png | 128x32 | 32x32 | 4 | 爆炸动画序列：帧0 白色闪光 -> 帧1 橙色火球扩散 -> 帧2 大范围红橙爆炸 -> 帧3 暗红色烟雾消散 |

## 瓦片集 (Tilesets)

包含多个地图瓦片的图集，按水平方向排列各瓦片，适合用于 Tilemap 地图绘制。

### tileset.png - 基础瓦片集

图片大小: 64x16，包含 4 个 16x16 瓦片。

| 瓦片索引 | 偏移 (x) | 瓦片大小 | 说明 |
|----------|----------|----------|------|
| 0 | 0 | 16x16 | 草地 (Grass)，上部绿色草皮、下部棕色泥土，带草丛纹理 |
| 1 | 16 | 16x16 | 泥土 (Dirt)，棕色泥土地面，带深色纹理颗粒 |
| 2 | 32 | 16x16 | 砖块 (Brick)，红棕色砖墙，带灰色砂浆线条，交错砌筑图案 |
| 3 | 48 | 16x16 | 石头 (Stone)，灰色石块，带深浅色纹理变化 |

### tankmap.png - 坦克大战瓦片集

图片大小: 160x32，包含 5 个 32x32 瓦片，FC 坦克大战 (Battle City) 风格。

| 瓦片索引 | 偏移 (x) | 瓦片大小 | 说明 |
|----------|----------|----------|------|
| 0 | 0 | 32x32 | 砖块 (Brick)，橙棕色砖墙，黑色砂浆线，交错砌筑，可被炮弹击碎 |
| 1 | 32 | 32x32 | 铁墙 (Steel)，银灰色钢板，2x2 网格布局，带高光棱边和铆钉细节 |
| 2 | 64 | 32x32 | 草丛 (Forest)，多层深浅绿色树丛，坦克可从下方穿过 |
| 3 | 96 | 32x32 | 河流 (Water)，深蓝色水面，正弦波纹图案，带浅色波光 |
| 4 | 128 | 32x32 | 冰面 (Ice)，浅蓝白色冰面，对角渐变，带裂纹和高光反射点 |

## 其他图片

| 文件名 | 图片大小 | 说明 |
|--------|----------|------|
| demo.png | 802x633 | GameLib 示例截图，展示 Tilemap 双层滚动效果（含树木、角色、砖块等场景元素） |

## 使用示例

使用 GameLib.h 加载和绘制精灵：

```cpp
#include "GameLib.h"

int main() {
    GameLib game;
    game.Open(640, 480, "Sprite Demo", true);

    // 加载精灵
    int ship = game.LoadSprite("assets/player_ship.png");
    int coin = game.LoadSprite("assets/coin.png");

    // 加载爆炸动画精灵表 (4 帧, 每帧 32x32)
    int boom = game.LoadSprite("assets/explosion.png");

    int frame = 0;
    while (!game.IsClosed()) {
        game.Clear(COLOR_BLACK);

        // 绘制精灵
        game.DrawSprite(ship, 100, 200);
        game.DrawSprite(coin, 200, 200);

        // 绘制爆炸动画帧 (从精灵表中裁剪)
        game.DrawSpriteEx(boom, 300, 200, frame * 32, 0, 32, 32);

        if (game.IsKeyPressed(KEY_SPACE)) {
            frame = (frame + 1) % 4;
        }

        game.Update();
        game.WaitFrame(60);
    }
    return 0;
}
```

---

*生成脚本: generate_assets.py, extract_planes.py*
