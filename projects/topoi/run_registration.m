(* ::Package:: *)
(* ::Input:: *)
fileName1=ToString[$CommandLine[[4]]];
fileName2=ToString[$CommandLine[[5]]];
project=ToString[$CommandLine[[6]]];
Print[project]
Needs["GeneralUtilities`"]
(* ::Input:: *)
({i1,i2}={Import[fileName1],Import[fileName2]};
y12=ImageCorrespondingPoints[i1,i2];
z12=FindGeometricTransform[y12[[1]], y12[[2]]];
If[Length[y12[[1]]]>1 ,
   {filetemp=y12;
    Export["TransformMatrix"<>project<>fileName1<>"_"<>fileName2<>".csv",z12[[2,1]],"CSV"]},""];)
(* ::Input:: *)
