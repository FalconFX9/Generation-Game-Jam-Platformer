class GeneratorData:

    def __init__(self, seed=None, mv_chance=0.2, mv_chance_x=0.5, mv_chance_y=0.5, mv_chance_xy=True, max_gap=160, max_height=2500, pl_num=10, lvl_id=None, lvl_description=None):
        self.seed = seed
        self.mv_chance = mv_chance
        self.mv_chance_x = mv_chance_x
        self.mv_chance_y = mv_chance_y
        self.mv_chance_xy = mv_chance_xy
        self.max_gap = max_gap
        self.max_height = max_height
        self.pl_num = pl_num
        self.lvl_id = lvl_id
        self.lvl_description = lvl_description


levels = [
    GeneratorData(1243, 0, max_gap=120, max_height=1500, lvl_id=0, lvl_description='Intro'),
    GeneratorData(1864, 0, max_gap=120, max_height=1500, lvl_id=1, lvl_description='A second step'),
    GeneratorData(4084, 0.2, 0.5, 0, lvl_id=2, lvl_description='Ooo slidy'),
    GeneratorData(8764, 0.2, 0.5, 0, lvl_id=3, lvl_description='Platform go brr'),
    GeneratorData(4317, 0.2, 0.5, 0, lvl_id=4, lvl_description='Slider 3'),
    GeneratorData(1620, 0.2, 0, 0.5, lvl_id=5, lvl_description='Movin up and'),
    GeneratorData(9895, 0.2, 0, 0.5, lvl_id=6, lvl_description='down like'),
    GeneratorData(1696, 0.2, 0, 0.5, lvl_id=7, lvl_description='an elevator'),
    GeneratorData(4384, lvl_id=8, lvl_description='Up n Down'),
    GeneratorData(1067, lvl_id=9, lvl_description='Side to side'),
    GeneratorData(3529, lvl_id=10, lvl_description='Like a roller \n coaster'),
    GeneratorData(1433, 0.2, 0.5, 0, lvl_id=11, lvl_description='Tarzan'),
    GeneratorData(8824, 0.2, 0, 0.5, lvl_id=12, lvl_description='Getting  ̶o̶v̶e̶r̶ \n under it'),
    GeneratorData(8791, lvl_id=13, lvl_description='Woooo nice'),
    GeneratorData(9188, lvl_id=14, lvl_description='All activated'),
    GeneratorData(5211, max_gap=200, lvl_id=15, lvl_description='Fun times'),
    GeneratorData(6604, lvl_id=16, lvl_description='Idk anymore'),
    GeneratorData(9996, pl_num=30, lvl_id=17, lvl_description='A long boi'),
    GeneratorData(1608, pl_num=2, lvl_id=18, lvl_description='Tight space'),
    GeneratorData(274, mv_chance=0.8, lvl_id=19, lvl_description='Chaos'),
    GeneratorData(8064, mv_chance=0.8, pl_num=2, lvl_id=20, lvl_description='H E L L')
]
