(* ::Package:: *)
(* ::Input:: *)
fileName1=ToString[$CommandLine[[4]]];
fileName2=ToString[$CommandLine[[5]]];
imagename1=StringSplit[fileName1,"."][[1]];
imagename2=StringSplit[fileName2,"."][[1]];
Needs["GeneralUtilities`"]
(* ::Input:: *)
({i1,i2}={Import[fileName1],Import[fileName2]};
y12=ImageCorrespondingPoints[i1,i2];
z12=FindGeometricTransform[y12[[1]], y12[[2]]];
If[Length[y12[[1]]]>1 ,
   {filetemp=y12;
    Export["TransformMatrix"<>imagename1<>"_"<>imagename2<>".csv",z12[[2,1]],"CSV"]},""];)
(* ::Input:: *)
