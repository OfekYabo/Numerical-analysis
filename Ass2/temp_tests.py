    def grade_assignment_1(self):
        try:
            import assignment1

            R=RESTRICT_INVOCATIONS
            names=  ('f','a','b','n')
            valss=[(R(10)(f2) ,0  ,5  ,10 ),
                   (R(20)(f4) ,-2 ,4  ,20 ),
                   (R(50)(f3) ,-1 ,5  ,50 ),
                   (R(20)(f13),3  ,10 ,20 ),
                   (R(20)(f1) ,2  ,5  ,20 ),
                   (R(10)(f7) ,3  ,16 ,10 ),
                   (R(10)(f8) ,1  ,3  ,10 ),
                   (R(10)(f9) ,5  ,10 ,10 ),
                   (R(20)(f10), 0.1, 5, 20),
                   (R(50)(f11), 0.1, 1, 50),
                   (R(20)(f12), -2, 2, 20)
                   ]
            params=[dict(zip(names,vals)) for vals in valss]
            
            expected_results=[f2,f4,f3,f13,f1,f7,f8,f9, f10, f11, f12]
            
            func_error=[ #mean absolute error at 2n points within the [a,b] range
                    SAVEARGS(a=a,b=b,n=n)(
                        lambda fres,fexp,a,b,n: 
                            sum([
                                    abs(fres(x)-fexp(x)) 
                                    for x in uniform(low=a,high=b,size=2*n)
                                    ])/2/n 
                        )
                    for _,a,b,n in valss
                    ]

            repeats=1
       
            ass = assignment1.Assignment1()
            self.grade_assignment(ass.interpolate,params,'Assignment 1',func_error,expected_results,repeats)
        except Exception as e:
