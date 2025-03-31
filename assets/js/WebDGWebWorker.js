const edgeTable=[
    0x0  , 0x109, 0x203, 0x30a, 0x406, 0x50f, 0x605, 0x70c,
    0x80c, 0x905, 0xa0f, 0xb06, 0xc0a, 0xd03, 0xe09, 0xf00,
    0x190, 0x99 , 0x393, 0x29a, 0x596, 0x49f, 0x795, 0x69c,
    0x99c, 0x895, 0xb9f, 0xa96, 0xd9a, 0xc93, 0xf99, 0xe90,
    0x230, 0x339, 0x33 , 0x13a, 0x636, 0x73f, 0x435, 0x53c,
    0xa3c, 0xb35, 0x83f, 0x936, 0xe3a, 0xf33, 0xc39, 0xd30,
    0x3a0, 0x2a9, 0x1a3, 0xaa , 0x7a6, 0x6af, 0x5a5, 0x4ac,
    0xbac, 0xaa5, 0x9af, 0x8a6, 0xfaa, 0xea3, 0xda9, 0xca0,
    0x460, 0x569, 0x663, 0x76a, 0x66 , 0x16f, 0x265, 0x36c,
    0xc6c, 0xd65, 0xe6f, 0xf66, 0x86a, 0x963, 0xa69, 0xb60,
    0x5f0, 0x4f9, 0x7f3, 0x6fa, 0x1f6, 0xff , 0x3f5, 0x2fc,
    0xdfc, 0xcf5, 0xfff, 0xef6, 0x9fa, 0x8f3, 0xbf9, 0xaf0,
    0x650, 0x759, 0x453, 0x55a, 0x256, 0x35f, 0x55 , 0x15c,
    0xe5c, 0xf55, 0xc5f, 0xd56, 0xa5a, 0xb53, 0x859, 0x950,
    0x7c0, 0x6c9, 0x5c3, 0x4ca, 0x3c6, 0x2cf, 0x1c5, 0xcc ,
    0xfcc, 0xec5, 0xdcf, 0xcc6, 0xbca, 0xac3, 0x9c9, 0x8c0,
    0x8c0, 0x9c9, 0xac3, 0xbca, 0xcc6, 0xdcf, 0xec5, 0xfcc,
    0xcc , 0x1c5, 0x2cf, 0x3c6, 0x4ca, 0x5c3, 0x6c9, 0x7c0,
    0x950, 0x859, 0xb53, 0xa5a, 0xd56, 0xc5f, 0xf55, 0xe5c,
    0x15c, 0x55 , 0x35f, 0x256, 0x55a, 0x453, 0x759, 0x650,
    0xaf0, 0xbf9, 0x8f3, 0x9fa, 0xef6, 0xfff, 0xcf5, 0xdfc,
    0x2fc, 0x3f5, 0xff , 0x1f6, 0x6fa, 0x7f3, 0x4f9, 0x5f0,
    0xb60, 0xa69, 0x963, 0x86a, 0xf66, 0xe6f, 0xd65, 0xc6c,
    0x36c, 0x265, 0x16f, 0x66 , 0x76a, 0x663, 0x569, 0x460,
    0xca0, 0xda9, 0xea3, 0xfaa, 0x8a6, 0x9af, 0xaa5, 0xbac,
    0x4ac, 0x5a5, 0x6af, 0x7a6, 0xaa , 0x1a3, 0x2a9, 0x3a0,
    0xd30, 0xc39, 0xf33, 0xe3a, 0x936, 0x83f, 0xb35, 0xa3c,
    0x53c, 0x435, 0x73f, 0x636, 0x13a, 0x33 , 0x339, 0x230,
    0xe90, 0xf99, 0xc93, 0xd9a, 0xa96, 0xb9f, 0x895, 0x99c,
    0x69c, 0x795, 0x49f, 0x596, 0x29a, 0x393, 0x99 , 0x190,
    0xf00, 0xe09, 0xd03, 0xc0a, 0xb06, 0xa0f, 0x905, 0x80c,
    0x70c, 0x605, 0x50f, 0x406, 0x30a, 0x203, 0x109, 0x0   ];

const triTable =
    [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 8, 3, 9, 8, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 2, 10, 0, 2, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 8, 3, 2, 10, 8, 10, 9, 8, -1, -1, -1, -1, -1, -1, -1],
    [3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 11, 2, 8, 11, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 9, 0, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 11, 2, 1, 9, 11, 9, 8, 11, -1, -1, -1, -1, -1, -1, -1],
    [3, 10, 1, 11, 10, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 10, 1, 0, 8, 10, 8, 11, 10, -1, -1, -1, -1, -1, -1, -1],
    [3, 9, 0, 3, 11, 9, 11, 10, 9, -1, -1, -1, -1, -1, -1, -1],
    [9, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 3, 0, 7, 3, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 9, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 1, 9, 4, 7, 1, 7, 3, 1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 4, 7, 3, 0, 4, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1],
    [9, 2, 10, 9, 0, 2, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1],
    [2, 10, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4, -1, -1, -1, -1],
    [8, 4, 7, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 4, 7, 11, 2, 4, 2, 0, 4, -1, -1, -1, -1, -1, -1, -1],
    [9, 0, 1, 8, 4, 7, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1],
    [4, 7, 11, 9, 4, 11, 9, 11, 2, 9, 2, 1, -1, -1, -1, -1],
    [3, 10, 1, 3, 11, 10, 7, 8, 4, -1, -1, -1, -1, -1, -1, -1],
    [1, 11, 10, 1, 4, 11, 1, 0, 4, 7, 11, 4, -1, -1, -1, -1],
    [4, 7, 8, 9, 0, 11, 9, 11, 10, 11, 0, 3, -1, -1, -1, -1],
    [4, 7, 11, 4, 11, 9, 9, 11, 10, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 4, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 5, 4, 1, 5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, 5, 4, 8, 3, 5, 3, 1, 5, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 8, 1, 2, 10, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1],
    [5, 2, 10, 5, 4, 2, 4, 0, 2, -1, -1, -1, -1, -1, -1, -1],
    [2, 10, 5, 3, 2, 5, 3, 5, 4, 3, 4, 8, -1, -1, -1, -1],
    [9, 5, 4, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 11, 2, 0, 8, 11, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1],
    [0, 5, 4, 0, 1, 5, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1],
    [2, 1, 5, 2, 5, 8, 2, 8, 11, 4, 8, 5, -1, -1, -1, -1],
    [10, 3, 11, 10, 1, 3, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1],
    [4, 9, 5, 0, 8, 1, 8, 10, 1, 8, 11, 10, -1, -1, -1, -1],
    [5, 4, 0, 5, 0, 11, 5, 11, 10, 11, 0, 3, -1, -1, -1, -1],
    [5, 4, 8, 5, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1],
    [9, 7, 8, 5, 7, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 3, 0, 9, 5, 3, 5, 7, 3, -1, -1, -1, -1, -1, -1, -1],
    [0, 7, 8, 0, 1, 7, 1, 5, 7, -1, -1, -1, -1, -1, -1, -1],
    [1, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 7, 8, 9, 5, 7, 10, 1, 2, -1, -1, -1, -1, -1, -1, -1],
    [10, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3, -1, -1, -1, -1],
    [8, 0, 2, 8, 2, 5, 8, 5, 7, 10, 5, 2, -1, -1, -1, -1],
    [2, 10, 5, 2, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1],
    [7, 9, 5, 7, 8, 9, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 11, -1, -1, -1, -1],
    [2, 3, 11, 0, 1, 8, 1, 7, 8, 1, 5, 7, -1, -1, -1, -1],
    [11, 2, 1, 11, 1, 7, 7, 1, 5, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 8, 8, 5, 7, 10, 1, 3, 10, 3, 11, -1, -1, -1, -1],
    [5, 7, 0, 5, 0, 9, 7, 11, 0, 1, 0, 10, 11, 10, 0, -1],
    [11, 10, 0, 11, 0, 3, 10, 5, 0, 8, 0, 7, 5, 7, 0, -1],
    [11, 10, 5, 7, 11, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 0, 1, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 8, 3, 1, 9, 8, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1],
    [1, 6, 5, 2, 6, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 6, 5, 1, 2, 6, 3, 0, 8, -1, -1, -1, -1, -1, -1, -1],
    [9, 6, 5, 9, 0, 6, 0, 2, 6, -1, -1, -1, -1, -1, -1, -1],
    [5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8, -1, -1, -1, -1],
    [2, 3, 11, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 0, 8, 11, 2, 0, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 9, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1],
    [5, 10, 6, 1, 9, 2, 9, 11, 2, 9, 8, 11, -1, -1, -1, -1],
    [6, 3, 11, 6, 5, 3, 5, 1, 3, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 11, 0, 11, 5, 0, 5, 1, 5, 11, 6, -1, -1, -1, -1],
    [3, 11, 6, 0, 3, 6, 0, 6, 5, 0, 5, 9, -1, -1, -1, -1],
    [6, 5, 9, 6, 9, 11, 11, 9, 8, -1, -1, -1, -1, -1, -1, -1],
    [5, 10, 6, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 3, 0, 4, 7, 3, 6, 5, 10, -1, -1, -1, -1, -1, -1, -1],
    [1, 9, 0, 5, 10, 6, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1],
    [10, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4, -1, -1, -1, -1],
    [6, 1, 2, 6, 5, 1, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7, -1, -1, -1, -1],
    [8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6, -1, -1, -1, -1],
    [7, 3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9, -1],
    [3, 11, 2, 7, 8, 4, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1],
    [5, 10, 6, 4, 7, 2, 4, 2, 0, 2, 7, 11, -1, -1, -1, -1],
    [0, 1, 9, 4, 7, 8, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1],
    [9, 2, 1, 9, 11, 2, 9, 4, 11, 7, 11, 4, 5, 10, 6, -1],
    [8, 4, 7, 3, 11, 5, 3, 5, 1, 5, 11, 6, -1, -1, -1, -1],
    [5, 1, 11, 5, 11, 6, 1, 0, 11, 7, 11, 4, 0, 4, 11, -1],
    [0, 5, 9, 0, 6, 5, 0, 3, 6, 11, 6, 3, 8, 4, 7, -1],
    [6, 5, 9, 6, 9, 11, 4, 7, 9, 7, 11, 9, -1, -1, -1, -1],
    [10, 4, 9, 6, 4, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 10, 6, 4, 9, 10, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1],
    [10, 0, 1, 10, 6, 0, 6, 4, 0, -1, -1, -1, -1, -1, -1, -1],
    [8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 10, -1, -1, -1, -1],
    [1, 4, 9, 1, 2, 4, 2, 6, 4, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4, -1, -1, -1, -1],
    [0, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, 3, 2, 8, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1],
    [10, 4, 9, 10, 6, 4, 11, 2, 3, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 2, 2, 8, 11, 4, 9, 10, 4, 10, 6, -1, -1, -1, -1],
    [3, 11, 2, 0, 1, 6, 0, 6, 4, 6, 1, 10, -1, -1, -1, -1],
    [6, 4, 1, 6, 1, 10, 4, 8, 1, 2, 1, 11, 8, 11, 1, -1],
    [9, 6, 4, 9, 3, 6, 9, 1, 3, 11, 6, 3, -1, -1, -1, -1],
    [8, 11, 1, 8, 1, 0, 11, 6, 1, 9, 1, 4, 6, 4, 1, -1],
    [3, 11, 6, 3, 6, 0, 0, 6, 4, -1, -1, -1, -1, -1, -1, -1],
    [6, 4, 8, 11, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [7, 10, 6, 7, 8, 10, 8, 9, 10, -1, -1, -1, -1, -1, -1, -1],
    [0, 7, 3, 0, 10, 7, 0, 9, 10, 6, 7, 10, -1, -1, -1, -1],
    [10, 6, 7, 1, 10, 7, 1, 7, 8, 1, 8, 0, -1, -1, -1, -1],
    [10, 6, 7, 10, 7, 1, 1, 7, 3, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7, -1, -1, -1, -1],
    [2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9, -1],
    [7, 8, 0, 7, 0, 6, 6, 0, 2, -1, -1, -1, -1, -1, -1, -1],
    [7, 3, 2, 6, 7, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 3, 11, 10, 6, 8, 10, 8, 9, 8, 6, 7, -1, -1, -1, -1],
    [2, 0, 7, 2, 7, 11, 0, 9, 7, 6, 7, 10, 9, 10, 7, -1],
    [1, 8, 0, 1, 7, 8, 1, 10, 7, 6, 7, 10, 2, 3, 11, -1],
    [11, 2, 1, 11, 1, 7, 10, 6, 1, 6, 7, 1, -1, -1, -1, -1],
    [8, 9, 6, 8, 6, 7, 9, 1, 6, 11, 6, 3, 1, 3, 6, -1],
    [0, 9, 1, 11, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [7, 8, 0, 7, 0, 6, 3, 11, 0, 11, 6, 0, -1, -1, -1, -1],
    [7, 11, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 8, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 9, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, 1, 9, 8, 3, 1, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1],
    [10, 1, 2, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 3, 0, 8, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1],
    [2, 9, 0, 2, 10, 9, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1],
    [6, 11, 7, 2, 10, 3, 10, 8, 3, 10, 9, 8, -1, -1, -1, -1],
    [7, 2, 3, 6, 2, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [7, 0, 8, 7, 6, 0, 6, 2, 0, -1, -1, -1, -1, -1, -1, -1],
    [2, 7, 6, 2, 3, 7, 0, 1, 9, -1, -1, -1, -1, -1, -1, -1],
    [1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6, -1, -1, -1, -1],
    [10, 7, 6, 10, 1, 7, 1, 3, 7, -1, -1, -1, -1, -1, -1, -1],
    [10, 7, 6, 1, 7, 10, 1, 8, 7, 1, 0, 8, -1, -1, -1, -1],
    [0, 3, 7, 0, 7, 10, 0, 10, 9, 6, 10, 7, -1, -1, -1, -1],
    [7, 6, 10, 7, 10, 8, 8, 10, 9, -1, -1, -1, -1, -1, -1, -1],
    [6, 8, 4, 11, 8, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 6, 11, 3, 0, 6, 0, 4, 6, -1, -1, -1, -1, -1, -1, -1],
    [8, 6, 11, 8, 4, 6, 9, 0, 1, -1, -1, -1, -1, -1, -1, -1],
    [9, 4, 6, 9, 6, 3, 9, 3, 1, 11, 3, 6, -1, -1, -1, -1],
    [6, 8, 4, 6, 11, 8, 2, 10, 1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 3, 0, 11, 0, 6, 11, 0, 4, 6, -1, -1, -1, -1],
    [4, 11, 8, 4, 6, 11, 0, 2, 9, 2, 10, 9, -1, -1, -1, -1],
    [10, 9, 3, 10, 3, 2, 9, 4, 3, 11, 3, 6, 4, 6, 3, -1],
    [8, 2, 3, 8, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1],
    [0, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 9, 0, 2, 3, 4, 2, 4, 6, 4, 3, 8, -1, -1, -1, -1],
    [1, 9, 4, 1, 4, 2, 2, 4, 6, -1, -1, -1, -1, -1, -1, -1],
    [8, 1, 3, 8, 6, 1, 8, 4, 6, 6, 10, 1, -1, -1, -1, -1],
    [10, 1, 0, 10, 0, 6, 6, 0, 4, -1, -1, -1, -1, -1, -1, -1],
    [4, 6, 3, 4, 3, 8, 6, 10, 3, 0, 3, 9, 10, 9, 3, -1],
    [10, 9, 4, 6, 10, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 9, 5, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 4, 9, 5, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1],
    [5, 0, 1, 5, 4, 0, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1],
    [11, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5, -1, -1, -1, -1],
    [9, 5, 4, 10, 1, 2, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1],
    [6, 11, 7, 1, 2, 10, 0, 8, 3, 4, 9, 5, -1, -1, -1, -1],
    [7, 6, 11, 5, 4, 10, 4, 2, 10, 4, 0, 2, -1, -1, -1, -1],
    [3, 4, 8, 3, 5, 4, 3, 2, 5, 10, 5, 2, 11, 7, 6, -1],
    [7, 2, 3, 7, 6, 2, 5, 4, 9, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 4, 0, 8, 6, 0, 6, 2, 6, 8, 7, -1, -1, -1, -1],
    [3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0, -1, -1, -1, -1],
    [6, 2, 8, 6, 8, 7, 2, 1, 8, 4, 8, 5, 1, 5, 8, -1],
    [9, 5, 4, 10, 1, 6, 1, 7, 6, 1, 3, 7, -1, -1, -1, -1],
    [1, 6, 10, 1, 7, 6, 1, 0, 7, 8, 7, 0, 9, 5, 4, -1],
    [4, 0, 10, 4, 10, 5, 0, 3, 10, 6, 10, 7, 3, 7, 10, -1],
    [7, 6, 10, 7, 10, 8, 5, 4, 10, 4, 8, 10, -1, -1, -1, -1],
    [6, 9, 5, 6, 11, 9, 11, 8, 9, -1, -1, -1, -1, -1, -1, -1],
    [3, 6, 11, 0, 6, 3, 0, 5, 6, 0, 9, 5, -1, -1, -1, -1],
    [0, 11, 8, 0, 5, 11, 0, 1, 5, 5, 6, 11, -1, -1, -1, -1],
    [6, 11, 3, 6, 3, 5, 5, 3, 1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 9, 5, 11, 9, 11, 8, 11, 5, 6, -1, -1, -1, -1],
    [0, 11, 3, 0, 6, 11, 0, 9, 6, 5, 6, 9, 1, 2, 10, -1],
    [11, 8, 5, 11, 5, 6, 8, 0, 5, 10, 5, 2, 0, 2, 5, -1],
    [6, 11, 3, 6, 3, 5, 2, 10, 3, 10, 5, 3, -1, -1, -1, -1],
    [5, 8, 9, 5, 2, 8, 5, 6, 2, 3, 8, 2, -1, -1, -1, -1],
    [9, 5, 6, 9, 6, 0, 0, 6, 2, -1, -1, -1, -1, -1, -1, -1],
    [1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8, 2, 6, 2, 8, -1],
    [1, 5, 6, 2, 1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 3, 6, 1, 6, 10, 3, 8, 6, 5, 6, 9, 8, 9, 6, -1],
    [10, 1, 0, 10, 0, 6, 9, 5, 0, 5, 6, 0, -1, -1, -1, -1],
    [0, 3, 8, 5, 6, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [10, 5, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 5, 10, 7, 5, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 5, 10, 11, 7, 5, 8, 3, 0, -1, -1, -1, -1, -1, -1, -1],
    [5, 11, 7, 5, 10, 11, 1, 9, 0, -1, -1, -1, -1, -1, -1, -1],
    [10, 7, 5, 10, 11, 7, 9, 8, 1, 8, 3, 1, -1, -1, -1, -1],
    [11, 1, 2, 11, 7, 1, 7, 5, 1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 11, -1, -1, -1, -1],
    [9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 11, 7, -1, -1, -1, -1],
    [7, 5, 2, 7, 2, 11, 5, 9, 2, 3, 2, 8, 9, 8, 2, -1],
    [2, 5, 10, 2, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1],
    [8, 2, 0, 8, 5, 2, 8, 7, 5, 10, 2, 5, -1, -1, -1, -1],
    [9, 0, 1, 5, 10, 3, 5, 3, 7, 3, 10, 2, -1, -1, -1, -1],
    [9, 8, 2, 9, 2, 1, 8, 7, 2, 10, 2, 5, 7, 5, 2, -1],
    [1, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 7, 0, 7, 1, 1, 7, 5, -1, -1, -1, -1, -1, -1, -1],
    [9, 0, 3, 9, 3, 5, 5, 3, 7, -1, -1, -1, -1, -1, -1, -1],
    [9, 8, 7, 5, 9, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [5, 8, 4, 5, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1],
    [5, 0, 4, 5, 11, 0, 5, 10, 11, 11, 3, 0, -1, -1, -1, -1],
    [0, 1, 9, 8, 4, 10, 8, 10, 11, 10, 4, 5, -1, -1, -1, -1],
    [10, 11, 4, 10, 4, 5, 11, 3, 4, 9, 4, 1, 3, 1, 4, -1],
    [2, 5, 1, 2, 8, 5, 2, 11, 8, 4, 5, 8, -1, -1, -1, -1],
    [0, 4, 11, 0, 11, 3, 4, 5, 11, 2, 11, 1, 5, 1, 11, -1],
    [0, 2, 5, 0, 5, 9, 2, 11, 5, 4, 5, 8, 11, 8, 5, -1],
    [9, 4, 5, 2, 11, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 5, 10, 3, 5, 2, 3, 4, 5, 3, 8, 4, -1, -1, -1, -1],
    [5, 10, 2, 5, 2, 4, 4, 2, 0, -1, -1, -1, -1, -1, -1, -1],
    [3, 10, 2, 3, 5, 10, 3, 8, 5, 4, 5, 8, 0, 1, 9, -1],
    [5, 10, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2, -1, -1, -1, -1],
    [8, 4, 5, 8, 5, 3, 3, 5, 1, -1, -1, -1, -1, -1, -1, -1],
    [0, 4, 5, 1, 0, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, 4, 5, 8, 5, 3, 9, 0, 5, 0, 3, 5, -1, -1, -1, -1],
    [9, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 11, 7, 4, 9, 11, 9, 10, 11, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 4, 9, 7, 9, 11, 7, 9, 10, 11, -1, -1, -1, -1],
    [1, 10, 11, 1, 11, 4, 1, 4, 0, 7, 4, 11, -1, -1, -1, -1],
    [3, 1, 4, 3, 4, 8, 1, 10, 4, 7, 4, 11, 10, 11, 4, -1],
    [4, 11, 7, 9, 11, 4, 9, 2, 11, 9, 1, 2, -1, -1, -1, -1],
    [9, 7, 4, 9, 11, 7, 9, 1, 11, 2, 11, 1, 0, 8, 3, -1],
    [11, 7, 4, 11, 4, 2, 2, 4, 0, -1, -1, -1, -1, -1, -1, -1],
    [11, 7, 4, 11, 4, 2, 8, 3, 4, 3, 2, 4, -1, -1, -1, -1],
    [2, 9, 10, 2, 7, 9, 2, 3, 7, 7, 4, 9, -1, -1, -1, -1],
    [9, 10, 7, 9, 7, 4, 10, 2, 7, 8, 7, 0, 2, 0, 7, -1],
    [3, 7, 10, 3, 10, 2, 7, 4, 10, 1, 10, 0, 4, 0, 10, -1],
    [1, 10, 2, 8, 7, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 9, 1, 4, 1, 7, 7, 1, 3, -1, -1, -1, -1, -1, -1, -1],
    [4, 9, 1, 4, 1, 7, 0, 8, 1, 8, 7, 1, -1, -1, -1, -1],
    [4, 0, 3, 7, 4, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 8, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 9, 3, 9, 11, 11, 9, 10, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 10, 0, 10, 8, 8, 10, 11, -1, -1, -1, -1, -1, -1, -1],
    [3, 1, 10, 11, 3, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 11, 1, 11, 9, 9, 11, 8, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 9, 3, 9, 11, 1, 2, 9, 2, 11, 9, -1, -1, -1, -1],
    [0, 2, 11, 8, 0, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 2, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 3, 8, 2, 8, 10, 10, 8, 9, -1, -1, -1, -1, -1, -1, -1],
    [9, 10, 2, 0, 9, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 3, 8, 2, 8, 10, 0, 1, 8, 1, 10, 8, -1, -1, -1, -1],
    [1, 10, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 3, 8, 9, 1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 9, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 3, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]];


onmessage = function (e) {

    // Ignore React DevTools messages
    if (!e.data.from_webdg) {
        console.warn("Ignoring nonsense sent to webworker. This is normal with some developer browser extensions.");
        return;
    }

    try {
        let obj;

        if (e.data.subject === "render_embbeded_curve") {
            obj = createEmbeddedCurveOBJ(e.data.ec_params);
            postMessage({ success: true, obj_file: obj});
        } else if (e.data.subject === "render_surface") {
            let S = createSurfaceOBJ(e.data.s_params);
            obj = S[0];
            vertexColorJSON = S[1];
            postMessage({ success: true, obj_file: obj, colorJSON : vertexColorJSON});
        } else if (e.data.subject === "render_curve") {
            obj = createCurveJSON(e.data.c_params);
            postMessage({ success: true, obj_file: obj});
        } else if (e.data.subject === "render_level_surface") {
            let LS = createLevelSurfaceOBJ(e.data.ls_params);
            obj = LS[0];
            postMessage({ success: true, obj_file: obj});
        } else {
            console.warn("The webworker was called with an ambiguous context.", e.data.subject);
            postMessage({ success: false});
            return;
        }

       

    } catch (error) {
        console.error("An error occurred:", error);
        postMessage({ success: false, error: error.message});
    }
};


// CURVE--------------------------------------------------------

function createCurveJSON(params) {
    importScripts('https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js');

    // Parse numeric params
    const nt = Math.max(2, params.nt);
    const t_start = math.evaluate(params.t_start);
    const t_end = math.evaluate(params.t_end);

    if (t_start > t_end) {
        [t_start, t_end] = [t_end, t_start]; // Swap if needed
    }

    const color_by = params.color_by;
    const color_hex = params.color_picker || "#FFFFFF";  // Default to white if no color is provided

    function hexToRGB(hex) {
        const bigint = parseInt(hex.slice(1), 16);
        return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
    }
    
    const solidColor = hexToRGB(color_hex);
    

    // Define the input for alpha (t)
    const alphaCompiled = [
        math.parse(params.x),
        math.parse(params.y),
        math.parse(params.z)
    ];

    // Derivatives for alpha', alpha'', alpha'''
    const alphaPrimeCompiled = [
        math.derivative(params.x, 't'),
        math.derivative(params.y, 't'),
        math.derivative(params.z, 't')
    ];

    const alphaDoublePrimeCompiled = [
        math.derivative(alphaPrimeCompiled[0].toString(), 't'),
        math.derivative(alphaPrimeCompiled[1].toString(), 't'),
        math.derivative(alphaPrimeCompiled[2].toString(), 't')
    ];

    const alphaTripplePrimeCompiled = [
        math.derivative(alphaDoublePrimeCompiled[0].toString(), 't'),
        math.derivative(alphaDoublePrimeCompiled[1].toString(), 't'),
        math.derivative(alphaDoublePrimeCompiled[2].toString(), 't')
    ];

    // Speed
    const speed = math.parse(
        `norm([${alphaPrimeCompiled[0]}, ${alphaPrimeCompiled[1]}, ${alphaPrimeCompiled[2]}]) / 1`
    );
    
    // Curvature :(
    const curvature = math.parse("norm(cross([" + alphaPrimeCompiled[0] + ", " + alphaPrimeCompiled[1] + ", " + alphaPrimeCompiled[2] + "], [" + alphaDoublePrimeCompiled[0] + ", " + alphaDoublePrimeCompiled[1] + ", " + alphaDoublePrimeCompiled[2] + "])) / (norm([" + alphaPrimeCompiled[0] + ", " + alphaPrimeCompiled[1] + ", " + alphaPrimeCompiled[2] + "]) ^ 3)");

    // Torsion :((
    const torsion = math.parse(
        "dot(cross([" + alphaPrimeCompiled[0] + ", " + alphaPrimeCompiled[1] + ", " + alphaPrimeCompiled[2] + "], [" + alphaDoublePrimeCompiled[0] + ", " + alphaDoublePrimeCompiled[1] + ", " + alphaDoublePrimeCompiled[2] + "]), [" + alphaTripplePrimeCompiled[0] + ", " + alphaTripplePrimeCompiled[1] + ", " + alphaTripplePrimeCompiled[2] + "]) / (norm(cross([" + alphaPrimeCompiled[0] + ", " + alphaPrimeCompiled[1] + ", " + alphaPrimeCompiled[2] + "], [" + alphaDoublePrimeCompiled[0] + ", " + alphaDoublePrimeCompiled[1] + ", " + alphaDoublePrimeCompiled[2] + "])) ^ 2)"
        );

    // Prepare for curvature and torsion calculations
    let curveData = {
        vertices: [],
        colors: [],
        speed: [],
        curvature: [],
        torsion: [],
        alpha : alphaCompiled.toString(),
        alphaPrime : alphaPrimeCompiled.toString(),
        alphaDoublePrime : alphaDoublePrimeCompiled.toString(),
        curvature_expression : curvature,
        torsion_expression : torsion
    };

    // Loop over the parameter t to calculate curvature and torsion
    for (let i = 0; i <= nt; i++) {
        const t = t_start + (i / nt) * (t_end - t_start);
        const scope = { t };

        // Evaluate position (alpha)
        const x = alphaCompiled[0].evaluate(scope);
        const y = alphaCompiled[1].evaluate(scope);
        const z = alphaCompiled[2].evaluate(scope);
        curveData.vertices.push([x, y, z]);

        // Evaluate curvature and torsion
        const spe = speed.evaluate(scope);  // Evaluate curvature
        const cur = curvature.evaluate(scope);  // Evaluate curvature
        const tor = torsion.evaluate(scope);    // Evaluate torsion
        
        // Store the results
        curveData.speed.push(spe);
        curveData.curvature.push(cur);
        curveData.torsion.push(tor);

        // Assign colors based on the selected mode
        let color;
        if (color_by === "Solid Color") {
            color = solidColor;
        } else if (color_by === "xyz") {
            color = [(255 * math.abs(x)) % 255,(255 * math.abs(y)) % 255,(255 * math.abs(z)) % 255]; 
        } else if (color_by === "Speed") {
            color = [speed];  // Color based on speed (simplified)
        } else if (color_by === "Curvature") {
            color = [curvature];  // Color based on curvature (simplified)
        } else if (color_by === "Torsion") {
            color = [torsion];  // Color based on torsion (simplified)
        } else if (color_by === "t") {
            color = [255 * i / nt, 255 * i / nt, 255 * i / nt];  // Color based on torsion (simplified)
        } else {
            color = [1, 1, 1]; // Default to white
        }

        curveData.colors.push(color);
    }


    // Find the min and max of the speed, curvature and torsion arrays
    const minSpeed = Math.min(...curveData.speed);
    const maxSpeed = Math.max(...curveData.speed);

    const minCurvature = Math.min(...curveData.curvature);
    const maxCurvature = Math.max(...curveData.curvature);

    const minTorsion = Math.min(...curveData.torsion);
    const maxTorsion = Math.max(...curveData.torsion);

    function interpolateColor(value, colorScale) {
        if (!Array.isArray(colorScale) || colorScale.length === 0) {
            throw new Error("colorScale must be a non-empty array.");
        }
    
        value = Math.min(1, Math.max(0, value)); // Clamp value to [0, 1]
    
        let scaledIndex = value * (colorScale.length - 1);
        let index = Math.floor(scaledIndex);
        let t = scaledIndex - index;
    
        // Ensure we don't go out of bounds
        if (index >= colorScale.length - 1) {
            return colorScale[colorScale.length - 1];
        }
    
        let c0 = colorScale[index];
        let c1 = colorScale[index + 1];
    
        // Check if c0 or c1 is undefined
        if (!c0 || !c1) {
            throw new Error("Invalid color value at index " + index);
        }
    
        return [
            Math.round(c0[0] + t * (c1[0] - c0[0])),
            Math.round(c0[1] + t * (c1[1] - c0[1])),
            Math.round(c0[2] + t * (c1[2] - c0[2]))
        ];
    }
    
    
    function getDivergingColor(value) {
            const colorScale = [
                [48, 18, 59],   // Deep Blue (Low)
                [70, 107, 190], // Blue (Middle-Low)
                [255, 216, 53], // Yellow (Middle-High)
                [189, 28, 33]   // Red (High)
            ];
            return interpolateColor(value, colorScale);
        }
        
    

    // Normalize and scale color values after the loop
    curveData.colors = curveData.colors.map((color, index) => {
        let spe = curveData.speed[index]; // Get the corresponding curvature value
        let cur = curveData.curvature[index]; // Get the corresponding curvature value
        let tor = curveData.torsion[index];   // Get the corresponding torsion value

        if (color_by === "Curvature") {
            // Handle division by zero case
            if (maxCurvature - minCurvature === 0 || maxCurvature - minCurvature < 0.00001) {
                return getDivergingColor(0.5); // Or you can return 0, depending on your preference
            }
            // Map the curvature value from min-max to 0-255
            let normalizedCurvature = ((cur - minCurvature) / (maxCurvature - minCurvature));
            return getDivergingColor(normalizedCurvature);
        } else if (color_by === "Torsion") {
            // Handle division by zero case
            if (maxTorsion - minTorsion === 0 || maxTorsion - minTorsion < 0.00001) {
                return getDivergingColor(0.5); // Or you can return 0, depending on your preference
            }
            // Map the torsion value from min-max to 0-255
            let normalizedTorsion = ((tor - minTorsion) / (maxTorsion - minTorsion));
            return getDivergingColor(normalizedTorsion);
        } else if (color_by === "Speed") {
            // Handle division by zero case
            if (maxSpeed - minSpeed === 0 || maxSpeed - minSpeed < 0.00001) {
                return getDivergingColor(0.5); // Or you can return 0, depending on your preference
            }
            // Map the Speed value from min-max to 0-255
            let normalizedSpeed = ((spe - minSpeed) / (maxSpeed - minSpeed));

            return getDivergingColor(normalizedSpeed);
        }

        return color;  // If not Speed, Curvature or Torsion, return the original color
    });




    return curveData;
}


// SURFACE-----------------------------------------------------

function createSurfaceOBJ(params) {

    // Helper function to interpolate between two hex colors
    function interpolateColorS(color1, color2, factor) {
        let c1 = hexToRgbS(color1);
        let c2 = hexToRgbS(color2);

        let r = Math.round(c1.r + factor * (c2.r - c1.r));
        let g = Math.round(c1.g + factor * (c2.g - c1.g));
        let b = Math.round(c1.b + factor * (c2.b - c1.b));

        return [r,g,b];
    }

    // Convert hex color to RGB
    function hexToRgbS(hex) {
        let bigint = parseInt(hex.slice(1), 16);
        return {
            r: (bigint >> 16) & 255,
            g: (bigint >> 8) & 255,
            b: bigint & 255
        };
    }

    function mapToCividis(value) {
        // Ensure value is within the expected range [-1, 1]
        value = Math.max(-1, Math.min(1, value));
    
        // Define the Cividis color scale manually (from Plotly's colormap)
        const cividisScale = [
            [-1, "#313695"],
            [-0.8, "#4575b4"],
            [-0.6, "#74add1"],
            [-0.4, "#abd9e9"],
            [-0.2, "#e0f3f8"],
            [0, "#ffffbf"],
            [0.2, "#fee090"],
            [0.4, "#fdae61"],
            [0.6, "#f46d43"],
            [0.8, "#d73027"],
            [1.0, "#A50026"]
        ];
    
        // Find the two closest points in the scale
        for (let i = 0; i < cividisScale.length - 1; i++) {
            let [t1, color1] = cividisScale[i];
            let [t2, color2] = cividisScale[i + 1];
    
            if (value >= t1 && value <= t2) {
                // Compute interpolation factor
                let factor = (value - t1) / (t2 - t1);
    
                // Interpolate between colors
                // [hexToRgb(color1).r, hexToRgb(color1).g, hexToRgb(color1).b];
                return interpolateColorS(color1, color2, factor);
            }
        }
    
        // Default return (shouldn't be reached)
        return [0, 0, 0];
    }

    //console.log("The validated: ", params);

    importScripts('https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js');

    //console.log("All the params made a");

    const { s_nu_validated, s_nv_validated, s_uend_validated, s_ustart_validated, s_vend_validated, s_vstart_validated, s_x_validated, s_y_validated, s_z_validated, s_colorby } = params;

    const uStart = math.evaluate(s_ustart_validated);
    const uEnd = math.evaluate(s_uend_validated);
    const vStart = math.evaluate(s_vstart_validated);
    const vEnd = math.evaluate(s_vend_validated);

    const uSteps = s_nu_validated;
    const vSteps = s_nv_validated;

    let objString = "# OBJ file with normals\n";

    function evalXYZ(u, v) {
        return {
            x: math.evaluate(s_x_validated, { u, v }),
            y: math.evaluate(s_y_validated, { u, v }),
            z: math.evaluate(s_z_validated, { u, v })
        };
    }

    function crossProduct(a, b) {
        return {
            x: a.y * b.z - a.z * b.y,
            y: a.z * b.x - a.x * b.z,
            z: a.x * b.y - a.y * b.x
        };
    }

    function normalize(v) {
        const length = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
        return { x: v.x / length, y: v.y / length, z: v.z / length };
    }

    const du = (uEnd - uStart) / uSteps;
    const dv = (vEnd - vStart) / vSteps;

    let minCurvature = 0;
    let maxCurvature = 0;
    let vertexCurvature = 0;

    let x_expr, y_expr, z_expr;
    let dx_du, dy_du, dz_du;
    let dx_dv, dy_dv, dz_dv;
    let d2x_du2, d2y_du2, d2z_du2;
    let d2x_dudv, d2y_dudv, d2z_dudv;
    let d2x_dv2, d2y_dv2, d2z_dv2;

    let E, F, G, L, M, N, K, H, k_1, k_2;
    

    if (s_colorby === "gaussian" || s_colorby === "mean" || s_colorby === "k1" || s_colorby === "k2") {
        // Get the math expressions
        x_expr = s_x_validated;
        y_expr = s_y_validated;
        z_expr = s_z_validated;
        
        // Compute derivatives
        dx_du = math.derivative(x_expr, 'u');
        dy_du = math.derivative(y_expr, 'u');
        dz_du = math.derivative(z_expr, 'u');
        
        dx_dv = math.derivative(x_expr, 'v');
        dy_dv = math.derivative(y_expr, 'v');
        dz_dv = math.derivative(z_expr, 'v');
        
        d2x_du2 = math.derivative(dx_du, 'u');
        d2y_du2 = math.derivative(dy_du, 'u');
        d2z_du2 = math.derivative(dz_du, 'u');
        
        d2x_dudv = math.derivative(dx_du, 'v');
        d2y_dudv = math.derivative(dy_du, 'v');
        d2z_dudv = math.derivative(dz_du, 'v');
        
        d2x_dv2 = math.derivative(dx_dv, 'v');
        d2y_dv2 = math.derivative(dy_dv, 'v');
        d2z_dv2 = math.derivative(dz_dv, 'v');

        // Compute the first fundamental form matrix (E, F, G)
        E = math.simplify(`(${dx_du})^2 + (${dy_du})^2 + (${dz_du})^2`);
        
        F = math.simplify(`(${dx_du}) * (${dx_dv}) + (${dy_du}) * (${dy_dv}) + (${dz_du}) * (${dz_dv})`);

        G = math.simplify(`(${dx_dv})^2 + (${dy_dv})^2 + (${dz_dv})^2`);

        // Compute the cross product (normal vector n)
        let n_x = math.simplify(`(${dy_du}) * (${dz_dv}) - (${dz_du}) * (${dy_dv})`);
        let n_y = math.simplify(`(${dz_du}) * (${dx_dv}) - (${dx_du}) * (${dz_dv})`);
        let n_z = math.simplify(`(${dx_du}) * (${dy_dv}) - (${dy_du}) * (${dx_dv})`);

        // Compute the magnitude of the normal vector
        const magnitude = math.simplify(`sqrt((${n_x})^2 + (${n_y})^2 + (${n_z})^2)`);

        // Normalize the normal vector
        n_x = math.simplify(`(${n_x}) / (${magnitude})`);
        n_y = math.simplify(`(${n_y}) / (${magnitude})`);
        n_z = math.simplify(`(${n_z}) / (${magnitude})`);

        // Compute the second fundamental form components (L, M, N)
        L = math.simplify(`(${d2x_du2}) * (${n_x}) + (${d2y_du2}) * (${n_y}) + (${d2z_du2}) * (${n_z})`);
        M = math.simplify(`(${d2x_dudv}) * (${n_x}) + (${d2y_dudv}) * (${n_y}) + (${d2z_dudv}) * (${n_z})`);
        N = math.simplify(`(${d2x_dv2}) * (${n_x}) + (${d2y_dv2}) * (${n_y}) + (${d2z_dv2}) * (${n_z})`);

        let maxK = -Infinity, minK = Infinity;
        let maxH = -Infinity, minH = Infinity;
        let maxk1 = -Infinity, mink1 = Infinity;
        let maxk2 = -Infinity, mink2 = Infinity;

        //console.log("Fundamental forms calculated");

        if (s_colorby === "gaussian") {

            K = math.simplify(`((${L}) * (${N}) - (${M})^2) / ((${E}) * (${G}) - (${F})^2)`);

            for (let i = 0; i <= uSteps; i++) {
                for (let j = 0; j <= vSteps; j++) {

                    const u = uStart + i * du;
                    const v = vStart + j * dv;
            
                    let K_value = K.evaluate({ u, v });

                    maxK = Math.max(maxK, K_value);
                    minK = Math.min(minK, K_value);

                }
            }

            maxCurvature = maxK;
            minCurvature = minK;

        } else if (s_colorby === "mean") {

            H = math.simplify(`((${E}) * (${N}) - 2 * (${F}) * (${M}) + (${G}) * (${L})) / (2 * ((${E}) * (${G}) - (${F})^2))`);

            for (let i = 0; i <= uSteps; i++) {
                for (let j = 0; j <= vSteps; j++) {

                    const u = uStart + i * du;
                    const v = vStart + j * dv;
            
                    let H_value = H.evaluate({ u, v });

                    maxH = Math.max(maxH, H_value);
                    minH = Math.min(minH, H_value);

                }
            }

            maxCurvature = maxH;
            minCurvature = minH;

        } else if (s_colorby === "k1") {
            K = math.simplify(`((${L}) * (${N}) - (${M})^2) / ((${E}) * (${G}) - (${F})^2)`);
            H = math.simplify(`((${E}) * (${N}) - 2 * (${F}) * (${M}) + (${G}) * (${L})) / (2 * ((${E}) * (${G}) - (${F})^2))`);
            k_1 = math.simplify(`(${H}) + sqrt((${H})^2 - (${K}))`);

            for (let i = 0; i <= uSteps; i++) {
                for (let j = 0; j <= vSteps; j++) {

                    const u = uStart + i * du;
                    const v = vStart + j * dv;

                    let k_1_value = k_1.evaluate({ u, v });
                    
                    maxk1 = Math.max(maxk1, k_1_value);
                    mink1 = Math.min(mink1, k_1_value);

                }
            }

            maxCurvature = maxk1;
            minCurvature = mink1;
        } else if (s_colorby === "k2") {
            K = math.simplify(`((${L}) * (${N}) - (${M})^2) / ((${E}) * (${G}) - (${F})^2)`);
            H = math.simplify(`((${E}) * (${N}) - 2 * (${F}) * (${M}) + (${G}) * (${L})) / (2 * ((${E}) * (${G}) - (${F})^2))`);
            k_2 = math.simplify(`(${H}) - sqrt((${H})^2 - (${K}))`);

            for (let i = 0; i <= uSteps; i++) {
                for (let j = 0; j <= vSteps; j++) {
                    const u = uStart + i * du;
                    const v = vStart + j * dv;
            
                    let k_2_value = k_2.evaluate({ u, v });
                    
                    maxk2 = Math.max(maxk2, k_2_value);
                    mink2 = Math.min(mink2, k_2_value);
                }
            }

            maxCurvature = maxk2;
            minCurvature = mink2;
        }

        //console.log("Calculated curvature bounds of type ", s_colorby, minCurvature, maxCurvature);
        
        
    }

    function vertexColor(u,v,uNorm, vNorm, x, y, z) {

        if (s_colorby === "uv") {

            const r = 255 * uNorm;  
            const g = 255 * vNorm;  
            const b = 0; 
        
            return { r, g, b };

        } else if (s_colorby === "xyz") {

            const r = math.abs(x * 255) %  255;  
            const g = math.abs(y * 255) %  255;  
            const b = math.abs(z * 255) %  255; 
        
            return { r, g, b };

        } else if (s_colorby === "normal" || s_colorby === "lighting") {

            const r = 255;  
            const g = 255;  
            const b = 255; 

            // there modes are handled directly in p5
            // so just return white
        
            return { r, g, b };

        } else {

            if (s_colorby === "gaussian") {

                let K_value = K.evaluate({ u, v });
                vertexCurvature = K_value;

            } else if (s_colorby === "mean") {

                let H_value = H.evaluate({ u, v });
                vertexCurvature = H_value;

            } else if (s_colorby === "k1") {

                let k_1_value = k_1.evaluate({ u, v });
                vertexCurvature = k_1_value;

            } else if (s_colorby === "k2") {

                let k_2_value = k_2.evaluate({ u, v });
                vertexCurvature = k_2_value;

            }

        } 

        

        let vertexCurvature_normalized = 0;

        if (maxCurvature - minCurvature !== 0) {
            let maxAbsCurvature = Math.max(Math.abs(minCurvature), Math.abs(maxCurvature));
            
            if (vertexCurvature !== 0) {
                vertexCurvature_normalized = vertexCurvature / maxAbsCurvature;
            }
        }
        else {
            // If min and max curvatures are the same, set the normalized value to a default (e.g., 0.5)
            vertexCurvature_normalized = 0;
        }

        let vertexColor = mapToCividis(vertexCurvature_normalized);

        const r = vertexColor[0];  
        const g = vertexColor[1];  
        const b = vertexColor[2]; 
        
        return { r, g, b };
    }

    let vertexColors = [];  // Stores colors for each vertex

    // Create vertices & texture coordinates
    for (let i = 0; i <= uSteps; i++) {
        for (let j = 0; j <= vSteps; j++) {
            const u = uStart + i * du;
            const v = vStart + j * dv;

            const p = evalXYZ(u, v);
            const uNorm = i / uSteps;  // Normalize U (0 to 1)
            const vNorm = j / vSteps;  // Normalize V (0 to 1)

            objString += `v ${p.x} ${p.y} ${p.z}\n`;
            objString += `vt ${uNorm} ${vNorm}\n`;  // Texture coordinates

            // push the color for this vertex to a
            // dataframe to be passed to p5js to be read
            // to make a pixels graphics buffer
            // that is then applied as a texture

            // Compute color based on (u, v)
            const color = vertexColor(u,v,uNorm, vNorm, p.x, p.y,p.z);  // Replace with your function

            // Store color data (normalized to 0-255)
            vertexColors.push({ u: uNorm, v: vNorm, r: color.r, g: color.g, b: color.b, u_index : i, v_index : j});
        }
    }

    const vertexColorJSON = JSON.stringify(vertexColors);

    // Create normals (with boundary condition handling)
    for (let i = 0; i <= uSteps; i++) {
        for (let j = 0; j <= vSteps; j++) {
            const u = uStart + i * du;
            const v = vStart + j * dv;

            const p = evalXYZ(u, v);
            const pu = evalXYZ(u + 1e-5, v);
            const pv = evalXYZ(u, v + 1e-5);

            const duVec = { x: pu.x - p.x, y: pu.y - p.y, z: pu.z - p.z };
            const dvVec = { x: pv.x - p.x, y: pv.y - p.y, z: pv.z - p.z };

            const normal = normalize(crossProduct(duVec, dvVec));

            objString += `vn ${normal.x} ${normal.y} ${normal.z}\n`;
        }
    }

    // Create faces (fix boundary faces)
    for (let i = 0; i < uSteps; i++) {
        for (let j = 0; j < vSteps; j++) {
            const p1 = i * (vSteps + 1) + j + 1;
            const p2 = (i + 1) * (vSteps + 1) + j + 1;
            const p3 = (i + 1) * (vSteps + 1) + j + 2;
            const p4 = i * (vSteps + 1) + j + 2;

            objString += `f ${p1}/${p1}/${p1} ${p2}/${p2}/${p2} ${p3}/${p3}/${p3}\n`;
            objString += `f ${p1}/${p1}/${p1} ${p3}/${p3}/${p3} ${p4}/${p4}/${p4}\n`;
        }
    }

    //console.log("OBJ file with normals has been created.");

    return [objString, vertexColorJSON];
}


// LEVEL SURFACE-----------------------------------------------

function createLevelSurfaceOBJ(params) {

    // I'm leaving this as a serial implementation for now
    // since it can already make shapes in a reasonable amount of time
    // that my 1080ti struggles with

    importScripts('https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js');

    const {
        ls_f_validated: f_expr,
        ls_xstart_validated: xStart,
        ls_xend_validated: xEnd,
        ls_nx_validated: nx,
        ls_ystart_validated: yStart,
        ls_yend_validated: yEnd,
        ls_ny_validated: ny,
        ls_zstart_validated: zStart,
        ls_zend_validated: zEnd,
        ls_nz_validated: nz
    } = params;

    const cornerIndex = [0, 4, 3, 7, 1, 5, 2, 6];

    // Convert bounds and steps to numbers
    const xMin = parseFloat(xStart), xMax = parseFloat(xEnd);
    const yMin = parseFloat(yStart), yMax = parseFloat(yEnd);
    const zMin = parseFloat(zStart), zMax = parseFloat(zEnd);

    const dx = (xMax - xMin) / (nx - 1);
    const dy = (yMax - yMin) / (ny - 1);
    const dz = (zMax - zMin) / (nz - 1);

    // Compile the function
    const f = math.compile(f_expr);

    let vertices = [];
    let faces = [];
    let normals = [];

    function evalF(x, y, z) {
        return f.evaluate({ x, y, z });
    }

    class XYZ {
        // Represents a 3D point or vector with x, y, and z coordinates
        constructor(x = 0, y = 0, z = 0) {
            this.x = x;
            this.y = y;
            this.z = z;
        }
    }
    
    const fValues = new Float32Array(nx * ny * nz);
    const positions = new Array(nx * ny * nz); // Store XYZ objects to avoid repeated creation
    
    for (let i = 0; i < nx; i++) {
        for (let j = 0; j < ny; j++) {
            for (let k = 0; k < nz; k++) {
                let idx = i + nx * (j + ny * k);
                let x = xMin + i * dx;
                let y = yMin + j * dy;
                let z = zMin + k * dz;
                positions[idx] = new XYZ(x, y, z);
                fValues[idx] = evalF(x, y, z); // Compute once and store
            }
        }
    }

    class Triangle {
        // Represents a triangle consisting of three vertices
        constructor() {
            this.p = [new XYZ(0, 0, 0), new XYZ(0, 0, 0), new XYZ(0, 0, 0)];
        }
    }
    
    function VertexInterp(isolevel, p1, p2, valp1, valp2, out) {

        if (Math.abs(isolevel - valp1) < 1e-7) {
            out.x = p1.x;
            out.y = p1.y;
            out.z = p1.z;
            return out;
        }
        if (Math.abs(isolevel - valp2) < 1e-7) {
            out.x = p2.x;
            out.y = p2.y;
            out.z = p2.z;
            return out;
        }
        if (Math.abs(valp1 - valp2) < 1e-7) {
            out.x = p1.x;
            out.y = p1.y;
            out.z = p1.z;
            return out;
        }
    
        let mu = (isolevel - valp1) / (valp2 - valp1);
        out.x = p1.x + mu * (p2.x - p1.x);
        out.y = p1.y + mu * (p2.y - p1.y);
        out.z = p1.z + mu * (p2.z - p1.z);
        return out;
    }
    
    function Polygonise(grid, isolevel = 0) {
        // Determines the set of triangles representing the isosurface within a grid cell
        let cubeindex = 0; // Index into the edge table
        let vertlist = Array(12).fill().map(() => new XYZ()); // Allocate once
        
        // Determine which corners of the cube are inside the isosurface
        for (let i = 0; i < 8; i++) {
            if (grid.val[i] < isolevel) cubeindex |= (1 << i);
        }
        
        // If cube is completely inside or outside the surface, return 0
        if (edgeTable[cubeindex] === 0) return 0;
        
        // Compute the intersection points of the isosurface with the cube edges
        if (edgeTable[cubeindex] & 1)
            VertexInterp(isolevel, grid.p[0], grid.p[1], grid.val[0], grid.val[1], vertlist[0]);
        if (edgeTable[cubeindex] & 2)
            VertexInterp(isolevel, grid.p[1], grid.p[2], grid.val[1], grid.val[2], vertlist[1]);
        if (edgeTable[cubeindex] & 4)
            VertexInterp(isolevel, grid.p[2], grid.p[3], grid.val[2], grid.val[3], vertlist[2]);
        if (edgeTable[cubeindex] & 8)
            VertexInterp(isolevel, grid.p[3], grid.p[0], grid.val[3], grid.val[0], vertlist[3]);
        if (edgeTable[cubeindex] & 16)
            VertexInterp(isolevel, grid.p[4], grid.p[5], grid.val[4], grid.val[5], vertlist[4]);
        if (edgeTable[cubeindex] & 32)
            VertexInterp(isolevel, grid.p[5], grid.p[6], grid.val[5], grid.val[6], vertlist[5]);
        if (edgeTable[cubeindex] & 64)
            VertexInterp(isolevel, grid.p[6], grid.p[7], grid.val[6], grid.val[7], vertlist[6]);
        if (edgeTable[cubeindex] & 128)
            VertexInterp(isolevel, grid.p[7], grid.p[4], grid.val[7], grid.val[4], vertlist[7]);
        if (edgeTable[cubeindex] & 256)
            VertexInterp(isolevel, grid.p[0], grid.p[4], grid.val[0], grid.val[4], vertlist[8]);
        if (edgeTable[cubeindex] & 512)
            VertexInterp(isolevel, grid.p[1], grid.p[5], grid.val[1], grid.val[5], vertlist[9]);
        if (edgeTable[cubeindex] & 1024)
            VertexInterp(isolevel, grid.p[2], grid.p[6], grid.val[2], grid.val[6], vertlist[10]);
        if (edgeTable[cubeindex] & 2048)
            VertexInterp(isolevel, grid.p[3], grid.p[7], grid.val[3], grid.val[7], vertlist[11]);
        
        // Create triangles from the interpolated vertices
        let ntriang = 0;
        let triangles=[];

        for (let i = 0; triTable[cubeindex][i] !== -1; i += 3) {
            triangles[ntriang] = new Triangle();
            triangles[ntriang].p[0] = vertlist[triTable[cubeindex][i]];
            triangles[ntriang].p[1] = vertlist[triTable[cubeindex][i + 1]];
            triangles[ntriang].p[2] = vertlist[triTable[cubeindex][i + 2]];
            ntriang++;
        }
        
        return triangles; // Return the number of triangles generated
    }

    let all_triangles = [];

    // March through the grid
    for (let i = 0; i < nx - 1; i++) {
        for (let j = 0; j < ny - 1; j++) {
            for (let k = 0; k < nz - 1; k++) {
                let gridCell = { p: [], val: [] };
    
                for (let gx = 0; gx <= 1; gx++) {
                    for (let gy = 0; gy <= 1; gy++) {
                        for (let gz = 0; gz <= 1; gz++) {
                            let ind = cornerIndex[gz + 2 * gy + 4 * gx];
    
                            let idx = (i + gx) + nx * ((j + gy) + ny * (k + gz));
                            gridCell.p[ind] = positions[idx];  // Reuse precomputed XYZ objects
                            gridCell.val[ind] = fValues[idx];  // Reuse function values
                        }
                    }
                }
    
                let these_triangles = Polygonise(gridCell);
    
                if (these_triangles.length > 0) {
                    all_triangles.push(...these_triangles);
                }
            }
        }
    }

    function calculateNormal(v1, v2, v3) {
        let v21 = new XYZ(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z);
        let v31 = new XYZ(v3.x - v1.x, v3.y - v1.y, v3.z - v1.z);
    
        // Cross product
        let nx = v21.y * v31.z - v21.z * v31.y;
        let ny = v21.z * v31.x - v21.x * v31.z;
        let nz = v21.x * v31.y - v21.y * v31.x;
    
        // Normalize the normal
        let length = Math.sqrt(nx * nx + ny * ny + nz * nz);
        return `${nx / length} ${ny / length} ${nz / length}`;
    }

    let vertexIndex = 1; // Start at 1 for 1-indexing in OBJ format
    let normalIndex = 1; // Start at 1 for 1-indexing in OBJ format

    all_triangles.forEach(triangle => {
        let triangleVertices = triangle.p;

        // Add the vertices
        triangleVertices.forEach(vertex => {
            vertices.push(`${vertex.x} ${vertex.y} ${vertex.z}`);
        });
    
        // Calculate and add normals
        let normal = calculateNormal(triangle.p[0], triangle.p[1], triangle.p[2]);
        triangleVertices.forEach(() => {
            normals.push(`vn ${normal}`);
        });
        
        // Create face entries with both vertex and normal indices
        let face = `f ${vertexIndex}//${normalIndex} ${vertexIndex + 1}//${normalIndex + 1} ${vertexIndex + 2}//${normalIndex + 2}`;
        faces.push(face);

        // Update the indices for the next triangle
        vertexIndex += 3;
        normalIndex += 3;

      });

    // Create OBJ file content
    let objString = "# Generated OBJ file\n";
    
    objString += vertices.map(v => `v ${v}`).join("\n") + "\n";
    objString += normals.map(n => `vn ${n}`).join("\n") + "\n";
    objString += faces.join("\n") + "\n";

    return [objString];
}


// EMBEDDED CURE------------------------------------------------

function createEmbeddedCurveOBJ(params) {

    //console.log("OBJ of the embedded curve has been created.");

    return "I'm the embedded curve obj.";
}

