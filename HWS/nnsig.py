# AUTOGENERATED! DO NOT EDIT! File to edit: 03_NN_numpy.ipynb (unless otherwise specified).

__all__ = ['fetch', 'mnist', 'kaiming_uniform', 'kaiming_normal', 'stat', 'Linear', 'MSELoss', 'NNL', 'CELoss', 'SGD',
           'Adam', 'Sequential', 'Conv', 'naive', 'Conv_dump', 'Flatten']

# Cell
import numpy as np

# Cell
def fetch(url):
    import requests, hashlib, os, tempfile
    fp = os.path.join(tempfile.gettempdir(), hashlib.md5(url.encode('utf-8')).hexdigest())

    if os.path.isfile(fp):
        with open(fp, "rb") as f:
            dat = f.read()

    else:
        dat = requests.get(url).content
        with open(fp + ".tmp", "wb") as f:
            f.write(dat)

        os.rename(fp+".tmp", fp)

    return dat

# Cell
def mnist(url1="http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz", url2="http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz", url3="http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz", url4="http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"):
    # from geohot
    import gzip
    import numpy as np

    def parse(dat): return np.frombuffer(
        gzip.decompress(dat), dtype=np.uint8).copy()

    X_train = parse(fetch(url1))[0x10:].reshape((-1, 28, 28))
    Y_train = parse(fetch(url2))[8:]
    X_test = parse(fetch(url3))[0x10:].reshape((-1, 28, 28))
    Y_test = parse(fetch(url4))[8:]
    return X_train, Y_train, X_test, Y_test


# Cell
# inits
# add "t" dimension for convolution, not tested
def kaiming_uniform(h,w,t=None):
    if t is None:
        return np.random.uniform(-1.,1.,size=(h,w))/np.sqrt(h*w)
    else:
        return np.random.uniform(-1.,1.,size=(h,w,t))/np.sqrt(h*w)

# ref to pytorch to see how gain is calculated
# not tested
def kaiming_normal(h,w,gain=1):
    return np.random.randn(h,w)/np.sqrt(2./h)*gain

# Cell
def stat(x):
    """ get standard deviation and mean of matrix x"""
    avg = x.mean()
    std = np.square(x - avg).mean()
    return avg, std

# Cell
class Linear:
    def __init__(self,h,w,init_fn = kaiming_uniform):
        self.weight = init_fn(h,w)
        self.grad = np.zeros((h,w))
        self.fpass = None

    def forward(self,x):
        out = x @ self.weight
        self.fpass = x
        return out

    def backward(self,bpass):
        self.grad = (self.fpass.T) @ bpass
        # without returning it, it doesn't work
        # bpass = bpass @ (self.weight.T)

# Cell
def MSELoss(yhat,y,num_class=10,supervised=True):
    if supervised:
        label = np.zeros((len(y), num_class), dtype=np.float32)
        label[range(label.shape[0]), y] = 1
        y = label
    val = np.square(yhat - y).mean(axis=0)
    grad = 2 * (yhat - y) / len(yhat)
    return val, grad

# can be achieved via NNL_Loss and softmax
def NNL():
    """ negative log likelihood """
    return

def CELoss(yhat,y):
    """ cross entropy loss"""
    return

# Cell
def SGD(lr = 1e-3, model = None):
    for layer in model:
        layer.weight -= lr * layer.grad

def Adam():
    pass

# Cell
class Sequential:
    # learn **kwargs
    def __init__(self,layers,lossfn,opt_fn):
        if not isinstance(layers,list):
            self.model = [layers]
        else:
            self.model = layers

        self.lossfn = lossfn
        self.opt_fn = opt_fn

    # check arguments when it comes to validation
    def forward(self,x):
        out = self.model[0].forward(x)
        for layer in self.model[1:]:
            out = layer.forward(out)
        return out

    def backward(self,grad):
        for layer in reversed(self.model):
            layer.backward(grad)
            grad = grad @ (layer.weight.T)

    def fit(self,x,y,epoch=1,batch_size=64,x_test=None,y_test=None):
        # loop thru len//bs
        losses = []
        ln = len(x)
        for _ in range(ln//batch_size):
            losses += self.fit_one_batch(x,y,epoch,batch_size,x_test,y_test)
        return losses

    def fit_one_batch(self,x,y,epoch=1,batch_size=64,x_test=None,y_test=None):
        # loop thru len//bs
        losses = []
        ln = len(x)
        for _ in range(epoch):
            idx = np.random.randint(0,ln,size=batch_size)
            x_ = x[idx].reshape((-1,28*28))
            y_ = y[idx]
            out = self.forward(x_)

            loss, grad = self.lossfn(out,y_)
            self.backward(grad)
            self.opt_fn(lr=1e-5, model=self.model)

            losses.append(loss.mean())

        return losses


# Cell
# not tested
class Conv:
    def __init__(self,filters,kernelsize,padding=0,init_fn=kaiming_uniform):
        self.weight = np.zeros((kernelsize,kernelsize,filters))
        for f in self.weight:
            f = init_fn(kernelsize,kernelsize)
        self.grad = np.zeros((kernelsize,kernelsize,filter))
        self.fpass = None

    def forward(self,x):
        # take advantage of einsum for speed and simplicity
        # assume x.shape[0] == x.shape[1]
        # ...
        return

    def backward(self,grad):
        # transpose weight to calculate gradient ?
        return

# Cell
# naive function of convolution
# to be compact, requires to calculate the general form of input/output dim and relationship between them
# now, let's use quick fix for default case
def naive(f,x,st=2,ks=3):
    out = np.zeros((((x.shape[0]-ks)//st+1),((x.shape[1]-ks)//st+1)))
    for i in range(0,x.shape[0]-1,st):
        for j in range(0,x.shape[1]-1,st):
            # for debug
            # print(i,":",i+ks,"->",j,":",j+ks)
            # print(x[i:i+ks,j:j+ks])

            # if shape are not the same: break
            if x[i:i+ks,j:j+ks].shape[0] != ks or x[i:i+ks,j:j+ks].shape[1] != ks:
                break
            out[i//st,j//st] = np.multiply(f,x[i:i+ks,j:j+ks]).sum()

    return out


# Cell
# can be used to test Conv class
# add Conv in naive way

"""
        About the loop: should try to reduce the time of walking thru input feature
        now: loop filters{loop thru input} ## SLOW
        faster version will be to loop thru every filter at the inner-est loop, then loop thru input
         , which will give us #walking thru = 1
"""
class Conv_dump:
    def __init__(self,filters=1,kernelsize=3,stride=2,padding=0,init_fn=kaiming_uniform):
        self.f = init_fn(kernelsize,kernelsize,filters)
        self.grad = np.zeros((kernelsize,kernelsize,filters))
        self.fpass = None
        self.ks = kernelsize
        self.st = stride

    def forward(self,x):
        # pre cache, don't know if it's actually faster compare to refering to self.sth every time
        f = self.f
        ks = self.ks
        st = self.st

        out = np.zeros((((x.shape[0]-ks)//st+1),((x.shape[1]-ks)//st+1),f.shape[-1]))
        """## DEBUG
        # now, it's slow
        for k in range(f.shape[-1]):
            out[:,:,k] = naive(f[:,:,k],x)
        """
        # then the input feature map
        for i in range(0,x.shape[0]-1,st):
            for j in range(0,x.shape[1]-1,st):
                # loop thru every filter first
                for k in range(f.shape[-1]):
                    if x[i:i+ks,j:j+ks,k].shape != (ks,ks):
                        break
                    out[i//st,j//st,k] = np.multiply(f,x[i:i+ks,j:j+ks]).sum()

        self.fpass = x
        return out

    def backward(self,bpass):
        # transpose weight to calculate gradient ?
        # loop
        #   x = input[i:i+ks,j:j+ks] # rth ks*ks matrix
        #   y = rth element in grad
        #   grad_per_step = x*y
        # convops
        # return it
        ftr = self.f.shape[-1]
        ks = self.ks
        st = self.st

        grad = np.zeros((ks,ks,ftr))
        fpass = self.fpass
        for i in range(0,fpass.shape[0]-1,st):
            for j in range(0,fpass.shape[1]-1,st):
                # iterative thru each filter so we don't have to re-run the whole input feature
                for k in range(ftr):
                    if fpass[i:i+ks,j:j+ks].shape[0] != ks or fpass[i:i+ks,j:j+ks].shape[1] != ks:
                        break
                    #print(bpass.shape,fpass[i:i+ks,j:j+ks,k].shape)
                    grad[:,:,k] += np.multiply(bpass[i//2,j//2,k],fpass[i:i+ks,j:j+ks,k])

        self.grad = grad

        # return the backproped gradient ?

# Cell
# not tested: 90% certain it's correct
# we're only use library (numpy)
# since it's slow to do computation in pure python
class Flatten:
    """
    reshape input to target shape
    """
    def __init__(self):
        self.shape=None

    def forward(self,x):
        """
        Should consider batch size
        image: (h,w,c) -> (b,h,w,c)
         flatten: (b,h*w*c)

        otherwise:
        (b,d) -> (1, b*d)

        """
        if self.shape is None:
            self.shape = x.shape
        if len(x.shape) < 3:
            return x.reshape((1,-1))
        return x.reshape((x.shape[0],-1))

    def backward(self,grad):
        return grad.reshape(self.shape)