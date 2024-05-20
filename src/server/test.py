from fastapi.routing import APIRouter
import matplotlib.pyplot as plt
from starlette.responses import FileResponse

import src.globals as g

router = APIRouter(

)


@router.get("/metrix")
def metrix():
    X_train, X_test, y_train, y_test = g.data
    y_pred = y_test.copy()
    y_pred[:] = g.model1.predict(X_test)
    y_pred_r = y_pred.copy()
    y_pred_r[:] = g.ss["y1"].inverse_transform(y_pred)
    y_test_r = y_test.copy()
    y_test_r[:] = g.ss["y1"].inverse_transform(y_test)
    plt.scatter(y_test_r.index, y_test_r, marker='.')
    plt.scatter(y_pred_r.index, y_pred_r, marker='.')
    plt.legend(["test", "pred"])
    plt.savefig("data/last.png")
    return FileResponse("data/last.png")
