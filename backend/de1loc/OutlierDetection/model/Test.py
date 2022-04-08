from OutlierDetection import OutlierDetection
import numpy as np

def TestOutlier():
    X = np.array(
        [
            [
                0.0, 0.0
            ],
            [
                1.0, 0.0
            ],
            [
                0.0, 1.0
            ],
            [
                4.0, 4.0
            ]
        ]
    )
    model = OutlierDetection(2,0.7,3,100,initial_data=X)
    test = model.add(np.array([[0.1,0.3]]), debug=True)
    print(test)
    assert(not test)
    test = model.add(np.array([[54.0,4.0]]), debug=True)
    print(test)
    assert(test)
    test = model.add(np.array([[54.0, 4.1]]), debug=True)
    print(test)
    assert(not test)

if __name__ == '__main__':
    TestOutlier()
