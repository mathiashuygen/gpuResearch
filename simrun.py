import carla
import time


def load_town(client, town):
    world = client.get_world()
    s = world.get_settings()

    # Save previous settings
    prev_no_render = s.no_rendering_mode
    prev_sync = s.synchronous_mode
    prev_dt = s.fixed_delta_seconds

    try:
        # Reduce load during map switch
        s.no_rendering_mode = True
        s.synchronous_mode = False
        s.fixed_delta_seconds = None
        world.apply_settings(s)

        time.sleep(1.0)
        print(f"Loading {town} ...")
        world = client.load_world(town, reset_settings=False)

        # Keep lightweight until streaming completes
        s2 = world.get_settings()
        s2.no_rendering_mode = True
        s2.synchronous_mode = False
        s2.fixed_delta_seconds = None
        world.apply_settings(s2)

        time.sleep(10.0)
        for _ in range(40):
            world.wait_for_tick(3.0)

        print("Loaded map:", world.get_map().name)

    finally:
        # Re-enable rendering if you need sensors/camera output
        w = client.get_world()
        s3 = w.get_settings()
        s3.no_rendering_mode = prev_no_render
        s3.synchronous_mode = prev_sync
        s3.fixed_delta_seconds = prev_dt
        w.apply_settings(s3)


def main():
    client = carla.Client("127.0.0.1", 2000)
    client.set_timeout(120.0)
    print("Server version:", client.get_server_version())

    # Try larger map
    load_town(client, "Town03")


if __name__ == "__main__":
    main()
