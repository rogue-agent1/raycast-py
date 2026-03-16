#!/usr/bin/env python3
"""2D raycaster — cast rays against line segments."""
import sys,math

def ray_segment(ox,oy,dx,dy,x1,y1,x2,y2):
    """Returns t (ray parameter) or None if no intersection."""
    sx,sy=x2-x1,y2-y1
    denom=dx*sy-dy*sx
    if abs(denom)<1e-10:return None
    t=((x1-ox)*sy-(y1-oy)*sx)/denom
    u=((x1-ox)*dy-(y1-oy)*dx)/denom
    if t>=0 and 0<=u<=1:return t
    return None

def cast_rays(ox,oy,segments,n_rays=360):
    hits=[]
    for i in range(n_rays):
        angle=2*math.pi*i/n_rays
        dx,dy=math.cos(angle),math.sin(angle)
        closest=float('inf')
        for x1,y1,x2,y2 in segments:
            t=ray_segment(ox,oy,dx,dy,x1,y1,x2,y2)
            if t is not None and t<closest:closest=t
        hits.append((angle,closest if closest<float('inf') else None))
    return hits

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        # Ray from origin going right, segment at x=5
        t=ray_segment(0,0,1,0, 5,-5,5,5)
        assert t is not None and abs(t-5)<1e-10
        # Ray going left misses
        t2=ray_segment(0,0,-1,0, 5,-5,5,5)
        assert t2 is None
        # Parallel ray
        t3=ray_segment(0,0,1,0, 0,1,10,1)
        assert t3 is None
        # Box
        box=[(0,0,10,0),(10,0,10,10),(10,10,0,10),(0,10,0,0)]
        hits=cast_rays(5,5,box,36)
        assert all(h[1] is not None for h in hits),"Rays inside box should all hit"
        print("All tests passed!")
    else:
        walls=[(0,0,100,0),(100,0,100,100),(100,100,0,100),(0,100,0,0)]
        hits=cast_rays(50,50,walls,8)
        for angle,dist in hits:
            print(f"  {math.degrees(angle):6.1f}° → {dist:.1f}" if dist else f"  {math.degrees(angle):6.1f}° → miss")
if __name__=="__main__":main()
