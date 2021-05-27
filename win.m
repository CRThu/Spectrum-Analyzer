weight = [1, 1.985844164102, 1.791176438506, 1.282075284005,0.667777530266, 0.240160796576, 0.056656381764, 0.008134974479,0.000624544650, 0.000019808998, 0.000000132974]

N = 256;
ind = (0:N-1)'*2*pi/(N-1);
w = weight(1)-  weight(2)*cos(ind) +  weight(3)*cos(2*ind)-  weight(4)*cos(3*ind) +  weight(5)*cos(4*ind)-  weight(6)*cos(5*ind) +  weight(7)*cos(6*ind)-  weight(8)*cos(7*ind) +  weight(9)*cos(8*ind)-  weight(10)*cos(9*ind) +  weight(11)*cos(10*ind)

wvtool(w)


weight = [1, 1.942604, 1.340318, 0.440811, 0.043097]

N = 256;
ind = (0:N-1)'*2*pi/(N-1);
w = weight(1)-  weight(2)*cos(ind) +  weight(3)*cos(2*ind)-  weight(4)*cos(3*ind) +  weight(5)*cos(4*ind)

wvtool(w)

