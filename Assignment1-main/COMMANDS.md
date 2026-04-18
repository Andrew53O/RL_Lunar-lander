# Seeded Experiment Commands

| Run Name | Run? |
| --- | --- |
| `v_base_s101` | [c] |
| `v_base_s202` | [c] |
| `v_base_s303` | [c] |
| `v_eps993_s101` | [c] |
| `v_eps993_s202` | [c] |
| `v_eps993_s303` | [c] |
| `v_eps997_s101` | [c] |
| `v_eps997_s202` | [c] |
| `v_eps997_s303` | [c] |
| `v_target5_s101` | [c] |
| `v_target5_s202` | [c] |
| `v_target5_s303` | [c] |
| `v_target20_s101` | [c] |
| `v_target20_s202` | [c] |
| `v_target20_s303` | [c] |
| `v_lr2p5e4_s101` | [c] |
| `v_lr2p5e4_s202` | [c] |
| `v_lr2p5e4_s303` | [c] |
| `v_lr1e3_s101` | [c] |
| `v_lr1e3_s202` | [c] |
| `v_lr1e3_s303` | [c] |

## `v_base_s101`

```bash
python main.py --device cpu --run-name v_base_s101 --seed 101
```

## `v_base_s202`

```bash
python main.py --device cpu --run-name v_base_s202 --seed 202
```

## `v_base_s303`

```bash
python main.py --device cpu --run-name v_base_s303 --seed 303
```

## `v_eps993_s101`

```bash
python main.py --device cpu --run-name v_eps993_s101 --epsilon-decay 0.993 --seed 101
```

## `v_eps993_s202`

```bash
python main.py --device cpu --run-name v_eps993_s202 --epsilon-decay 0.993 --seed 202
```

## `v_eps993_s303`

```bash
python main.py --device cpu --run-name v_eps993_s303 --epsilon-decay 0.993 --seed 303
```

## `v_eps997_s101`

```bash
python main.py --device cpu --run-name v_eps997_s101 --epsilon-decay 0.997 --seed 101
```

## `v_eps997_s202`

```bash
python main.py --device cpu --run-name v_eps997_s202 --epsilon-decay 0.997 --seed 202
```

## `v_eps997_s303`

```bash
python main.py --device cpu --run-name v_eps997_s303 --epsilon-decay 0.997 --seed 303
```

## `v_target5_s101`

```bash
python main.py --device cpu --run-name v_target5_s101 --target-update-freq 5 --seed 101
```

## `v_target5_s202`

```bash
python main.py --device cpu --run-name v_target5_s202 --target-update-freq 5 --seed 202
```

## `v_target5_s303`

```bash
python main.py --device cpu --run-name v_target5_s303 --target-update-freq 5 --seed 303
```

## `v_target20_s101`

```bash
python main.py --device cpu --run-name v_target20_s101 --target-update-freq 20 --seed 101
```

## `v_target20_s202`

```bash
python main.py --device cpu --run-name v_target20_s202 --target-update-freq 20 --seed 202
```

## `v_target20_s303`

```bash
python main.py --device cpu --run-name v_target20_s303 --target-update-freq 20 --seed 303
```

## `v_lr2p5e4_s101`

```bash
python main.py --device cpu --run-name v_lr2p5e4_s101 --learning-rate 2.5e-4 --seed 101
```

## `v_lr2p5e4_s202`

```bash
python main.py --device cpu --run-name v_lr2p5e4_s202 --learning-rate 2.5e-4 --seed 202
```

## `v_lr2p5e4_s303`

```bash
python main.py --device cpu --run-name v_lr2p5e4_s303 --learning-rate 2.5e-4 --seed 303
```

## `v_lr1e3_s101`

```bash
python main.py --device cpu --run-name v_lr1e3_s101 --learning-rate 1e-3 --seed 101
```

## `v_lr1e3_s202`

```bash
python main.py --device cpu --run-name v_lr1e3_s202 --learning-rate 1e-3 --seed 202
```

## `v_lr1e3_s303`

```bash
python main.py --device cpu --run-name v_lr1e3_s303 --learning-rate 1e-3 --seed 303
```
