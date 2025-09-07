import numpy as np

# 地球半径（公里）
EARTH_RADIUS = 6371.0


def great_circle_distance(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """
    计算地球表面两点之间的大圆距离（Haversine公式）
    
    参数:
        lat1, lon1: 第一个点的纬度和经度（度）
        lat2, lon2: 第二个点的纬度和经度（度）
        radius: 地球半径（默认6371公里）
    
    返回:
        float: 两点之间的距离（公里）
    """
    # 将经纬度转换为弧度
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # 哈维正弦公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    
    return c * radius  # 距离（公里）

def vincenty_distance(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """
    计算地球表面两点之间的距离（Vincenty公式，更精确但计算量更大）
    
    参数:
        lat1, lon1: 第一个点的纬度和经度（度）
        lat2, lon2: 第二个点的纬度和经度（度）
        radius: 地球半径（默认6371公里）
    
    返回:
        float: 两点之间的距离（公里）
    """
    # 将经纬度转换为弧度
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Vincenty公式
    a = 6378.137  # 赤道半径（公里）
    b = 6356.7523142  # 极半径（公里）
    f = (a - b) / a  # 扁率
    
    L = lon2 - lon1
    U1 = np.arctan((1 - f) * np.tan(lat1))
    U2 = np.arctan((1 - f) * np.tan(lat2))
    
    sinU1 = np.sin(U1)
    cosU1 = np.cos(U1)
    sinU2 = np.sin(U2)
    cosU2 = np.cos(U2)
    
    lambda_ = L
    lambda_prev = 2 * np.pi
    iter_limit = 20
    
    while np.abs(lambda_ - lambda_prev) > 1e-12 and iter_limit > 0:
        sinLambda = np.sin(lambda_)
        cosLambda = np.cos(lambda_)
        sinSigma = np.sqrt((cosU2 * sinLambda) ** 2 + 
                          (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        
        if sinSigma == 0:
            return 0  # 两点重合
        
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = np.arctan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cosSqAlpha = 1 - sinAlpha ** 2
        
        if cosSqAlpha != 0:
            cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        else:
            cos2SigmaM = 0  # 赤道上的线
        
        C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        lambda_prev = lambda_
        lambda_ = L + (1 - C) * f * sinAlpha * (
            sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM ** 2)))
        
        iter_limit -= 1
    
    # 计算最终距离
    if iter_limit == 0:
        # 迭代未收敛，回退到哈维正弦公式
        return great_circle_distance(lat1, lon1, lat2, lon2, radius)
    
    uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma * (-1 + 2 * cos2SigmaM ** 2) - 
                              B / 6 * cos2SigmaM * (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
    
    return b * A * (sigma - deltaSigma)