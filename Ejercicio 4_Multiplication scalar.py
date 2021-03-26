from Crypto.Util.number import inverse
# Point Addition in Elliptic Curve

p= 9739
a=497
b=1768

def add_points(p1,p2):
  # p1=(x1,y1) , p2=(x2,y2)
  
  if p1 == (0,0):
    return p2
  if p2 == (0,0):
    return p1
  # Revisar si este es iverso
  x1,y1=p1
  x2,y2=p2
  if x1==x2 and y1==-y2:
    return (0,0)

  if p1==p2:
    s1=( 3*pow(x1,2,p) + a ) % p
    s2=(2*y1)%p
    s=s1*inverse(s2,p)
  else:
    s1=(y2-y1)%p
    s2=(x2-x1)%p
    s=s1*inverse(s2,p)
  # Calculamos el punto ahora 
  x3=((s*s)-x1-x2)%p
  y3=(s*(x1-x3)-y1)%p
  return (x3,y3)

def scalar_mul(p,n):
  P = p
  Q = p
  R=(0,0) 
  while n>0:
    if n&1:
      R=add_points(R,Q)
    Q=add_points(Q,Q)
    n=n//2
  return R    

P = (2339, 2213)
S=scalar_mul(P,7863)
print(S)