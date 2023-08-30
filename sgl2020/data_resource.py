import pooch

Resource = pooch.create(
    path=pooch.os_cache("sgl2020"),
    base_url="http://lab-server.l4y.top:1145/sgl2020/",
    registry={
        "Flt1002_train.h5": "md5:d42e6579719e31d17115c9b8ed3e4471",
        "Flt1003_train.h5": "md5:bc0e819bebb8bc9d4814cdbce0fb911a",
        "Flt1004_train.h5": "md5:a17c1678407c02f260d7250b4e6c3a15",
        "Flt1005_train.h5": "md5:0065e0a270db7f53544ba8df247e1c12",
        "Flt1006_train.h5": "md5:fb798e26d515673deae2e1b349b9e215",
        "Flt1007_train.h5": "md5:ad29d8bb5ab8a3c97ac02b8f83b41b01",
    },
)
