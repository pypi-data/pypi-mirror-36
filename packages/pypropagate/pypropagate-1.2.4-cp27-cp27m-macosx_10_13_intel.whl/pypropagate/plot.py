
def get_metric_prefix(numbers):
    import numpy as np

    if not isinstance(numbers,list):
        numbers = list(numbers)
    if len(numbers) >= 2:
        numbers = [numbers[-1] - numbers[0]]

    def get_exponent(number):
        return int(np.log10(np.abs(number))) if number != 0 else 0

    from units import metric_prefixes

    exponents = [get_exponent(number) for number in numbers]
    largest = max(exponents,key=lambda x:abs(x))

    closest = min(metric_prefixes, key=lambda x:abs(x[1]+2-largest))

    return (closest[2],10**closest[1])

def get_unitless_bounds(array):

    from .units import get_unit

    bounds = []

    for l,r in array.bounds:
        unit = get_unit(l)
        if unit == None:
            unit = get_unit(r)
        try:
            if unit == None:
                bounds.append((float(l),float(r),1))
            else:
                bounds.append((float(l/unit),float(r/unit),unit))
        except:
            raise ValueError('Cannot convert to unitless expression: %s with unit: %s' % ((l,r),unit))

    return bounds

def get_plot_coordinates(array):
    import numpy as np
    from expresso.pycas import latex
    e = get_unitless_bounds(array)[0]
    prefix,factor = get_metric_prefix(e[:2])
    return np.linspace(float(e[0])/factor,float(e[1])/factor,array.shape[0]), prefix + ' ' + latex(e[2])


def image_plot(carr,ax = None,figsize = None,title = None, **kwargs):
    import matplotlib.pyplot as plt

    # fix missing \text support
    from expresso.pycas import latex as rlatex
    latex = lambda x:rlatex(x).replace(r'\text',r'\mathrm')

    fig = None
    if ax == None:
        fig, ax = plt.subplots(figsize=figsize)
    if title:
        ax.set_title(title)

    e = get_unitless_bounds(carr)

    xprefix,xfactor = get_metric_prefix(e[1][:2])
    yprefix,yfactor = get_metric_prefix(e[0][:2])

    extent = [float(e[1][0])/xfactor,float(e[1][1])/xfactor,float(e[0][0])/yfactor,float(e[0][1])/yfactor]

    if 'aspect' not in kwargs:
        kwargs['aspect'] = 'auto'
    if 'origin' not in kwargs:
        kwargs['origin'] = 'lower'

    image = ax.imshow(carr.data, extent=extent, **kwargs )
    ax.set_ylabel("$%s$ [$%s %s$]" % (latex(carr.axis[0]),yprefix,latex(e[0][2])))
    ax.set_xlabel("$%s$ [$%s %s$]" % (latex(carr.axis[1]),xprefix,latex(e[1][2])))

    if fig:
        fig.colorbar(image)
        plt.show()

    return image

def line_plot(carr,ax = None,ylabel = None,figsize = None,title = None,**kwargs):
    import matplotlib.pyplot as plt
    import numpy as np

    # fix missing \text support
    from expresso.pycas import latex as rlatex
    latex = lambda x:rlatex(x).replace(r'\text',r'\mathrm')

    fig = None
    if ax == None:
        fig, ax = plt.subplots(figsize=figsize)

    if title:
        ax.set_title(title)

    e = get_unitless_bounds(carr)[0]

    prefix,factor = get_metric_prefix(e[:2])

    lines = ax.plot(np.linspace(float(e[0])/factor,float(e[1])/factor,carr.data.shape[0]),carr.data, **kwargs)
    ax.set_xlabel("$%s$ [$%s %s$]" % (latex(carr.axis[0]),prefix,latex(e[2])))
    if ylabel: ax.set_ylabel(ylabel)

    if fig:
        plt.show()

    return lines[0]

def poynting_streamplot(carr,k,ax = None,figsize = None,title = None,set_limits = True,mask = None,support = None,settings=None,dxdy = None,**kwargs):
    import matplotlib.pyplot as plt
    import numpy as np
    import expresso.pycas as pc
    from .phase_gradient import phase_gradient   
 
    e = get_unitless_bounds(carr)

    xprefix,xfactor = get_metric_prefix(e[1][:2])
    yprefix,yfactor = get_metric_prefix(e[0][:2])

    extent = [float(e[1][0])/xfactor,float(e[1][1])/xfactor,float(e[0][0])/yfactor,float(e[0][1])/yfactor]

    x = np.linspace(extent[0],extent[1],carr.shape[1])
    y = np.linspace(extent[2],extent[3],carr.shape[0])

    if dxdy is None:
        gx,gy = [g.data for g in phase_gradient(carr)]
        gx /= xfactor*(x[0] - x[1])
        gy /= yfactor*(y[0] - y[1])
        gx += float(carr.evaluate(k*e[1][2]))
    else:
        gx,gy = dxdy

    gx *= yfactor/xfactor

    if support is not None:
        if mask is not None:
            raise ValueError('provide either support or mask arguments')

        if isinstance(support,pc.Expression):
            mask = pc.Not(support)
        else:
            mask = support.copy()
            mask.data = np.logical_not(support.data)

    if mask is not None:
        import expresso.pycas

        if isinstance(mask,pc.Expression):
            if settings == None:
                raise ValueError('no settings argument provided')
            mask = expression_for_array(mask,carr,settings)

        gx = np.ma.array(gx,mask=mask.data)
        gy = np.ma.array(gy,mask=mask.data)
        
    fig = None
    if ax == None:
        fig, ax = plt.subplots(figsize=figsize)
    if title:
        ax.set_title(title)

    stream = ax.streamplot(x,y,gx,gy,**kwargs)

    if set_limits:
        ax.set_xlim(extent[0],extent[1])
        ax.set_ylim(extent[2],extent[3])

    from expresso.pycas import latex as rlatex
    latex = lambda x:rlatex(x).replace(r'\text',r'\mathrm')
    ax.set_ylabel("$%s$ [$%s %s$]" % (latex(carr.axis[0]),yprefix,latex(e[0][2])))
    ax.set_xlabel("$%s$ [$%s %s$]" % (latex(carr.axis[1]),xprefix,latex(e[1][2])))

    if fig:
        plt.show()

    return stream

def poynting_streamplot_with_start_points(carr,k,start_points,color='w',ax = None,figsize = None,title = None,arrowsize=5,arrowpositions=[0.1,0.9],set_limits = True,mask = None,support = None,settings=None,dxdy = None,**kwargs):
    import matplotlib.pyplot as plt
    import numpy as np
    import expresso.pycas as pc
    from pypropagate.phase_gradient import phase_gradient
    
    def streamlines(x,y,U,V,start_points):
        import scipy as sci
        import scipy.integrate
        import scipy.interpolate
        import numpy as np

        N = len(start_points)
        flat_start_values = np.array(start_points).flatten()

        dt = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
        NT = max(len(x),len(y))
        norm = np.sqrt(U**2+V**2) * dt

        XY = (y,x)
        uinterp = sci.interpolate.RegularGridInterpolator(XY,U/norm,fill_value=0,bounds_error=False)
        vinterp = sci.interpolate.RegularGridInterpolator(XY,V/norm,fill_value=0,bounds_error=False)

        dx = [0]

        def interpolated_velocity(t,x):
            x = x.reshape((N,2))
            res = np.stack([vinterp(x),uinterp(x)]).transpose().flatten()
            dx[0] = res
            return res

        integrator = sci.integrate.ode(interpolated_velocity).set_integrator('dopri5')
        integrator.set_initial_value(flat_start_values, 0)

        integrated = np.zeros((NT,N,2),dtype=float)
        integrated[0] = start_points

        for i in range(1,NT):
            if not integrator.successful():
                print "error"
                break
            integrated[i] = integrator.integrate(i*dt).reshape((N,2))
            if np.all(dx[0] ==0):
                integrated = integrated[:i+1]
                break

        return integrated
    
    
    e = get_unitless_bounds(carr)

    xprefix,xfactor = get_metric_prefix(e[1][:2])
    yprefix,yfactor = get_metric_prefix(e[0][:2])

    extent = [float(e[1][0])/xfactor,float(e[1][1])/xfactor,float(e[0][0])/yfactor,float(e[0][1])/yfactor]

    x = np.linspace(extent[0],extent[1],carr.shape[1])
    y = np.linspace(extent[2],extent[3],carr.shape[0])

    if dxdy is None:
        gx,gy = phase_gradient(carr)
        gx /= xfactor*(x[0] - x[1])
        gy /= yfactor*(y[0] - y[1])
        gx += float(carr.evaluate(k*e[1][2]))
    else:
        gx,gy = dxdy

    gx *= yfactor/xfactor

    if support is not None:
        if mask is not None:
            raise ValueError('provide either support or mask arguments')

        if isinstance(support,pc.Expression):
            mask = pc.Not(support)
        else:
            mask = support.copy()
            mask.data = np.logical_not(support.data)

    if mask is not None:
        import expresso.pycas

        if isinstance(mask,pc.Expression):
            if settings == None:
                raise ValueError('no settings argument provided')
            mask = expression_for_array(mask,carr,settings)

        gx = np.ma.array(gx.data,mask=mask.data)
        gy = np.ma.array(gy.data,mask=mask.data)
        
    fig = None
    if ax == None:
        fig, ax = plt.subplots(figsize=figsize)
    if title:
        ax.set_title(title)
    
    start_points = [[float(carr.evaluate(sp[1]/(yfactor*e[0][2]))),float(carr.evaluate(sp[0]/(xfactor*e[1][2])))] for sp in start_points]
    stream = streamlines(x,y,gx.data,gy.data,start_points)

    for i in range(stream.shape[1]):
        ax.plot(stream[:,i,1],stream[:,i,0],'-',color=color,**kwargs)
   
        import scipy
        xmin,xmax = stream[:,i,1].min(),stream[:,i,1].max()
        dx  = (xmax - xmin) / len(stream[:,i,1]) / 10
        xpositions = [xmin + ap * (xmax - xmin) for ap in arrowpositions]  
        ypositions = scipy.interp(xpositions + [xp - dx for xp in xpositions],stream[:,i,1],stream[:,i,0])
        for i in range(len(arrowpositions)):
            size = arrowsize 
            x0,y0,y1 = xpositions[i],ypositions[i],ypositions[i+len(arrowpositions)]
	    props = dict( color=color, width=0, headwidth=size, headlength=2*size, linewidth=0)
	    ax.annotate("",xy=(x0,y0), xycoords='data', xytext=(x0-dx, y1), textcoords='data', arrowprops=props)
    
    if set_limits:
        ax.set_xlim(extent[0],extent[1])
        ax.set_ylim(extent[2],extent[3])

    from expresso.pycas import latex as rlatex
    latex = lambda x:rlatex(x).replace(r'\text',r'\mathrm')
    ax.set_ylabel("$%s$ [$%s %s$]" % (latex(carr.axis[0]),yprefix,latex(e[0][2])))
    ax.set_xlabel("$%s$ [$%s %s$]" % (latex(carr.axis[1]),xprefix,latex(e[1][2])))

    if fig:
        plt.show()

    return stream

def expression_to_array(expression, settings, axes = None, maxres=None):
    import expresso.pycas
    import numpy as np

    s = settings.simulation_box

    expr = settings.get_optimized(expression)


    if axes == None:
        sym = expresso.pycas.get_symbols_in(expr)
    else:
        sym = set()
        for a in axes:
            sym.add(expresso.pycas.Symbol(a.name + "_i"))

    if isinstance(sym,set):
        sym = set(sym)

    from .coordinate_ndarray import CoordinateNDArray

    #namedict = {key:name for name,key in zip(s.names(),s.keys())}
    def get_axis_name(symbol):
    #    name = namedict[symbol]
    #    return name[:-1]
        return symbol.name[:-2]

    if len(sym) == 0:
        c = complex(expr)
        if c.imag == 0:
            return c.real
        return c
        #raise ValueError('cannot create field: expression contains no symbols')
    elif len(sym) == 1:
        xi = sym.pop()
        xname = get_axis_name(xi)
        x = getattr(s,xname)
        keys = tuple([getattr(s,p % xname) for p in ['%smin','%smax','N%s']])
        xmin,xmax,nx = settings.get_numeric( keys )
        nx = settings.get_as( nx , int )
        npx = np.arange(nx)
        data =  expresso.pycas.numpyfy(expr)(**{xi.name:npx})
        res =  CoordinateNDArray(data,[(xmin,xmax)],(x,),settings.get_numeric_transform())
    elif len(sym) == 2:
        yi,xi = sorted([sym.pop(),sym.pop()],key = lambda x:x.name)[::-1]

        xname = get_axis_name(xi)
        yname = get_axis_name(yi)

        if xname == 't':
            xi,xname,yi,yname = yi,yname,xi,xname

        y,x = getattr(s,yname),getattr(s,xname)

        keys = tuple([getattr(s,p % i) for i in (xname,yname) for p in ['%smin','%smax','N%s']])
        xmin,xmax,nx,ymin,ymax,ny = settings.get_numeric( keys )
        nx,ny = settings.get_as( (nx,ny) , int )
        npy,npx = np.meshgrid(np.arange(ny),np.arange(nx))
        data =  expresso.pycas.numpyfy(expr,parallel=True)(**{xi.name:npx,yi.name:npy})
        res =  CoordinateNDArray(data,[(xmin,xmax),(ymin,ymax)],(x,y),settings.get_numeric_transform())
    else:
        raise ValueError('cannot create field: expression contains more than two free symbols: %s' % sym)

    return res


def expression_for_array(expr,array,settings):
    settings = settings.copy()
    for ax,b,s in zip(array.axis,array.bounds,array.shape):
        settings.simulation_box.unlock(ax.name + 'min')
        settings.simulation_box.unlock(ax.name + 'max')
        settings.simulation_box.unlock('N' + ax.name)
        setattr(settings.simulation_box,ax.name + 'min',b[0])
        setattr(settings.simulation_box,ax.name + 'max',b[1])
        setattr(settings.simulation_box,'N' + ax.name,s)
    return expression_to_array(expr,settings,axes=array.axis)


def plot(arg, *args, **kwargs):
    """
    Simple plot function for 1D and 2D coordinate arrays. If the data is complex, the absolute square value of the data will be plottted.

    Parameters
    -----------
    arg: coordinate array
          the input data

    **kwargs: additional parameters to be passed to the plot functions

    Returns
    --------
    plot: output of ax.plot for 1D and ax.imshow for 2D arrays

    """
    import expresso.pycas
    import numpy as np
    from coordinate_ndarray import CoordinateNDArray

    if isinstance(arg,expresso.pycas.Expression):
        from .settings import Settings

        if len(args) > 0 and isinstance(args[0],Settings):
            settings = args[0]
            args = list(args)
            del args[0]
        else:
            settings = kwargs.get('settings')
            if not settings:
                raise ValueError('cannot plot expression: no settings provided')
            del kwargs['settings']

        arg = expression_to_array(arg, settings)

        if isinstance(arg,(float,complex)):
            print arg
            return

    elif not isinstance(arg,CoordinateNDArray):
        if isinstance(arg,np.ndarray):
            pc = expresso.pycas
            arg = CoordinateNDArray(arg,[(pc.S(0),pc.S(n)) for n in arg.shape],[pc.Symbol('x_%i' % i) for i in range(len(arg.shape))])
        else:
            raise ValueError('cannot plot non CoordinateNDArray object. For plotting regular arrays please use the matplotlib.pyplot module.')

    if not np.can_cast(arg.data.dtype, np.float128):
        if np.all(arg.data.imag == 0): arg = arg.real
        else: arg = abs(arg) ** 2
    if len(arg.axis) == 1: return line_plot(arg, *args, **kwargs)
    elif len(arg.axis) == 2: return image_plot(arg, *args, **kwargs)
    else: raise ValueError("input array must be one or two dimensional")


def plot_poynting(array,k,ax = None,figsize=None,**kwargs):
    import matplotlib.pyplot as plt

    fig = None

    if ax == None: fig, ax = plt.subplots(figsize=figsize)
    if 'color' not in kwargs: kwargs['color']='w'

    image = image_plot(abs(array)**2,ax=ax)
    stream = poynting_streamplot(array,k,ax=ax,**kwargs)

    if fig:
        plt.colorbar(image)
        plt.show()

    return image,stream




