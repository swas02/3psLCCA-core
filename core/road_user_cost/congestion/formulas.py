from ... import standard_keys as c


def _cap_between_one_and_two(results: dict) -> dict:
    return {
        k: (1 if (x := v) < 1 else 2 if x > 2 else x)
        if isinstance(v, (int, float))
        else (_ for _ in ()).throw(ValueError(f"Non-numeric value for '{k}': {v}"))
        for k, v in results.items()
    }

# --------------------------------------------------------
# Table 10 – Time-Related Congestion Factors
# --------------------------------------------------------


def time_congestion_factors(lane_type: str, vc: float) -> dict:
    if type(vc) not in [int, float]:
        raise ValueError(
            f"Volume to capacity ratio 'vc' must be a number, got {type(vc)} instead.")

    if lane_type == c.SL:
        results = {
            c.SMALL_CARS: 0.747 + 1.458 * vc,
            c.BIG_CARS: 0.747 + 1.458 * vc,
            c.TWO_WHEELERS: 0.911 + 0.807 * vc,
            c.BUSES: 0.838 + 1.307 * vc,
            c.LCV: 0.880 + 1.200 * vc,
            c.HCV: 0.858 + 1.101 * vc,
            c.MCV: 0.858 + 1.101 * vc
        }

    elif lane_type == c.IL:
        results = {
            c.SMALL_CARS: 0.930 + 1.025 * vc,
            c.BIG_CARS: 0.930 + 1.025 * vc,
            c.TWO_WHEELERS: 0.776 + 0.728 * vc,
            c.BUSES: 0.942 + 0.670 * vc,
            c.LCV: 1.012 + 0.863 * vc,
            c.HCV: 0.920 + 1.033 * vc,
            c.MCV: 0.920 + 1.033 * vc
        }

    elif lane_type == c.L2:
        results = {
            c.SMALL_CARS: 1.087 + 0.483 * vc,
            c.BIG_CARS: 1.087 + 0.483 * vc,
            c.TWO_WHEELERS: 0.804 + 0.865 * vc,
            c.BUSES: 0.864 + 0.543 * vc,
            c.LCV: 0.925 + 0.573 * vc,
            c.HCV: 0.878 + 0.561 * vc,
            c.MCV: 0.878 + 0.561 * vc
        }

    elif lane_type == c.L4:
        results = {
            c.SMALL_CARS: 0.4834*(vc**2) + 0.4095*vc + 0.99,
            c.BIG_CARS: 0.4834*(vc**2) + 0.4095*vc + 0.99,
            c.TWO_WHEELERS: 1.1063*vc + 0.99,
            c.BUSES: 1.534*(vc**2) - 0.2301*vc + 0.99,
            c.LCV: 0.8441*(vc**2) + 0.4337*vc + 0.99,
            c.HCV: 1.1036*(vc**2) + 0.4124*vc + 0.99,
            c.MCV: 0.3709*(vc**2) + 0.4604*vc + 0.99
        }

    elif lane_type == c.L6:
        results = {
            c.SMALL_CARS: 2.1947*(vc**2) - 0.3352*vc + 1,
            c.BIG_CARS: 2.1947*(vc**2) - 0.3352*vc + 1,
            c.TWO_WHEELERS: 0.8998*(vc**2) + 0.9407*vc + 1,
            c.BUSES: 0.9412*(vc**2) - 0.1881*vc + 1,
            c.LCV: 0.8441*(vc**2) + 0.4337*vc + 0.99,
            c.HCV: 1.593*(vc**2) - 0.0523*vc + 1,
            c.MCV: 1.0234*vc + 1
        }

    elif lane_type in [c.L8, c.EW]:
        results = {
            c.SMALL_CARS: -0.2441*(vc**2) + 0.9003*vc + 0.99,
            c.BIG_CARS: -0.2441*(vc**2) + 0.9003*vc + 0.99,
            c.TWO_WHEELERS: 0.3973*vc + 1,
            c.BUSES: -0.0092*(vc**2) + 0.4559*vc + 1,
            c.LCV: -0.1476*(vc**2) + 0.5986*vc + 0.99,
            c.HCV: 0.2143*(vc**2) + 0.457*vc + 1,
            c.MCV: -0.373*(vc**2) + 0.7575*vc + 1
        }

    else:
        raise ValueError(f"Unknown lane type. Use {c.SL}, {c.IL}, {c.L2}, {c.L4}, {c.L6}, {c.L8}, {c.EW}.")


    return _cap_between_one_and_two(results)


# --------------------------------------------------------
# Table 11 – Distance-Related Congestion Factors
# --------------------------------------------------------
def distance_congestion_factors(lane_type: str, vc: float) -> dict:
    if type(vc) not in [int, float]:
        raise ValueError(f"'vc' must be numeric, got {type(vc)}")

    if lane_type == c.SL:
        results = {
            c.SMALL_CARS: 0.924 + 0.680 * vc,
            c.BIG_CARS: 0.924 + 0.680 * vc,
            c.TWO_WHEELERS: 0.990 + 0.830 * vc,
            c.BUSES: 1.000 + 1.000 * vc,
            c.LCV: 1.00 + 0.90 * vc,
            c.HCV: 1.179 + 0.757 * vc,
            c.MCV: 1.179 + 0.757 * vc
        }

    elif lane_type == c.IL:
        results = {
            c.SMALL_CARS: 0.924 + 0.635 * vc,
            c.BIG_CARS: 0.924 + 0.635 * vc,
            c.TWO_WHEELERS: 0.942 + 0.118 * vc,
            c.BUSES: 0.800 + 1.200 * vc,
            c.LCV: 0.90 + 1.00 * vc,
            c.HCV: 1.104 + 0.755 * vc,
            c.MCV: 1.104 + 0.755 * vc
        }

    elif lane_type == c.L2:
        results = {
            c.SMALL_CARS: 0.893 + 0.259 * vc,
            c.BIG_CARS: 0.893 + 0.259 * vc,
            c.TWO_WHEELERS: 0.917 + 0.112 * vc,
            c.BUSES: 0.800 + 1.10 * vc,
            c.LCV: 0.90 + 1.00 * vc,
            c.HCV: 0.925 + 0.482 * vc,
            c.MCV: 0.900 + 1.40 * vc
        }

    elif lane_type == c.L4:
        results = {
            c.SMALL_CARS: 2.4405*(vc**2) - 2.8919*vc + 1.8939,
            c.BIG_CARS: 3.713*(vc**2) - 4.2811*vc + 2.2173,
            c.TWO_WHEELERS: 4.9774*(vc**2) - 4.8846*vc + 2.1831,
            c.BUSES: 3.713*(vc**2) - 4.2811*vc + 2.2173,
            c.LCV: 2.2518*(vc**2) - 1.2471*vc + 1.1348,
            c.HCV: 2.8147*(vc**2) - 1.5589*vc + 1.4185,
            c.MCV: 3.6591*(vc**2) - 2.0266*vc + 1.8441
        }

    elif lane_type == c.L6:
        results = {
            c.SMALL_CARS: 2.8163*(vc**2) - 3.1278*vc + 1.9629,
            c.BIG_CARS: 4.3108*(vc**2) - 4.6276*vc + 2.3129,
            c.TWO_WHEELERS: 5.6528*(vc**2) - 4.5691*vc + 1.9083,
            c.BUSES: 4.3108*(vc**2) - 4.6276*vc + 2.3129,
            c.LCV: 14.990*(vc**2) - 12.014*vc + 3.2242,
            c.HCV: 18.737*(vc**2) - 15.017*vc + 4.0302,
            c.MCV: 24.3581*(vc**2) - 19.522*vc + 5.2393
        }

    elif lane_type in [c.L8, c.EW]:
        results = {
            c.SMALL_CARS: 0.5239*(vc**2) - 0.9289*vc + 1.4847,
            c.BIG_CARS: 0.7734*(vc**2) - 1.3037*vc + 1.596,
            c.TWO_WHEELERS: 2.4879*(vc**2) - 3.9095*vc + 2.6253,
            c.BUSES: 0.7734*(vc**2) - 1.3037*vc + 1.596,
            c.LCV: 0.7707*(vc**2) - 0.7214*vc + 1.0232,
            c.HCV: 0.9634*(vc**2) - 0.9018*vc + 1.279,
            c.MCV: 1.2524*(vc**2) - 1.1723*vc + 1.6627
        }

    else:
        raise ValueError(f"Unknown lane type. Use {c.SL}, {c.IL}, {c.L2}, {c.L4}, {c.L6}, {c.L8}, {c.EW}.")

    return _cap_between_one_and_two(results)
