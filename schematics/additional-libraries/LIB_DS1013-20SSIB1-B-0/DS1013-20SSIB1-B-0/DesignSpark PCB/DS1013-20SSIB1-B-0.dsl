SamacSys ECAD Model
15720371/1369245/2.50/20/3/Connector

DESIGNSPARK_INTERMEDIATE_ASCII

(asciiHeader
	(fileUnits MM)
)
(library Library_1
	(padStyleDef "c180_h120"
		(holeDiam 1.2)
		(padShape (layerNumRef 1) (padShapeType Ellipse)  (shapeWidth 1.8) (shapeHeight 1.8))
		(padShape (layerNumRef 16) (padShapeType Ellipse)  (shapeWidth 1.8) (shapeHeight 1.8))
	)
	(padStyleDef "s180_h120"
		(holeDiam 1.2)
		(padShape (layerNumRef 1) (padShapeType Rect)  (shapeWidth 1.8) (shapeHeight 1.8))
		(padShape (layerNumRef 16) (padShapeType Rect)  (shapeWidth 1.8) (shapeHeight 1.8))
	)
	(textStyleDef "Default"
		(font
			(fontType Stroke)
			(fontFace "Helvetica")
			(fontHeight 50 mils)
			(strokeWidth 5 mils)
		)
	)
	(patternDef "SHDR20W69P254X254_2X10_3300X91" (originalName "SHDR20W69P254X254_2X10_3300X91")
		(multiLayer
			(pad (padNum 1) (padStyleRef s180_h120) (pt 0, 0) (rotation 90))
			(pad (padNum 2) (padStyleRef c180_h120) (pt 0, 2.54) (rotation 90))
			(pad (padNum 3) (padStyleRef c180_h120) (pt 2.54, 0) (rotation 90))
			(pad (padNum 4) (padStyleRef c180_h120) (pt 2.54, 2.54) (rotation 90))
			(pad (padNum 5) (padStyleRef c180_h120) (pt 5.08, 0) (rotation 90))
			(pad (padNum 6) (padStyleRef c180_h120) (pt 5.08, 2.54) (rotation 90))
			(pad (padNum 7) (padStyleRef c180_h120) (pt 7.62, 0) (rotation 90))
			(pad (padNum 8) (padStyleRef c180_h120) (pt 7.62, 2.54) (rotation 90))
			(pad (padNum 9) (padStyleRef c180_h120) (pt 10.16, 0) (rotation 90))
			(pad (padNum 10) (padStyleRef c180_h120) (pt 10.16, 2.54) (rotation 90))
			(pad (padNum 11) (padStyleRef c180_h120) (pt 12.7, 0) (rotation 90))
			(pad (padNum 12) (padStyleRef c180_h120) (pt 12.7, 2.54) (rotation 90))
			(pad (padNum 13) (padStyleRef c180_h120) (pt 15.24, 0) (rotation 90))
			(pad (padNum 14) (padStyleRef c180_h120) (pt 15.24, 2.54) (rotation 90))
			(pad (padNum 15) (padStyleRef c180_h120) (pt 17.78, 0) (rotation 90))
			(pad (padNum 16) (padStyleRef c180_h120) (pt 17.78, 2.54) (rotation 90))
			(pad (padNum 17) (padStyleRef c180_h120) (pt 20.32, 0) (rotation 90))
			(pad (padNum 18) (padStyleRef c180_h120) (pt 20.32, 2.54) (rotation 90))
			(pad (padNum 19) (padStyleRef c180_h120) (pt 22.86, 0) (rotation 90))
			(pad (padNum 20) (padStyleRef c180_h120) (pt 22.86, 2.54) (rotation 90))
		)
		(layerContents (layerNumRef 18)
			(attr "RefDes" "RefDes" (pt 0, 0) (textStyleRef "Default") (isVisible True))
		)
		(layerContents (layerNumRef 30)
			(line (pt -5.32 -3.53) (pt -5.32 6.45) (width 0.05))
		)
		(layerContents (layerNumRef 30)
			(line (pt -5.32 6.45) (pt 28.43 6.45) (width 0.05))
		)
		(layerContents (layerNumRef 30)
			(line (pt 28.43 6.45) (pt 28.43 -3.53) (width 0.05))
		)
		(layerContents (layerNumRef 30)
			(line (pt 28.43 -3.53) (pt -5.32 -3.53) (width 0.05))
		)
		(layerContents (layerNumRef 28)
			(line (pt -5.07 -3.28) (pt -5.07 6.2) (width 0.1))
		)
		(layerContents (layerNumRef 28)
			(line (pt -5.07 6.2) (pt 28.18 6.2) (width 0.1))
		)
		(layerContents (layerNumRef 28)
			(line (pt 28.18 6.2) (pt 28.18 -3.28) (width 0.1))
		)
		(layerContents (layerNumRef 28)
			(line (pt 28.18 -3.28) (pt -5.07 -3.28) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(line (pt 0 -3.28) (pt 28.18 -3.28) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt 28.18 -3.28) (pt 28.18 6.2) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt 28.18 6.2) (pt -5.07 6.2) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -5.07 6.2) (pt -5.07 0) (width 0.2))
		)
	)
	(symbolDef "DS1013-20SSIB1-B-0" (originalName "DS1013-20SSIB1-B-0")

		(pin (pinNum 1) (pt 0 mils 0 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -25 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 2) (pt 0 mils -100 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -125 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 3) (pt 0 mils -200 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -225 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 4) (pt 0 mils -300 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -325 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 5) (pt 0 mils -400 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -425 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 6) (pt 0 mils -500 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -525 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 7) (pt 0 mils -600 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -625 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 8) (pt 0 mils -700 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -725 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 9) (pt 0 mils -800 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -825 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 10) (pt 0 mils -900 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -925 mils) (rotation 0]) (justify "Left") (textStyleRef "Default"))
		))
		(pin (pinNum 11) (pt 900 mils 0 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -25 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 12) (pt 900 mils -100 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -125 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 13) (pt 900 mils -200 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -225 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 14) (pt 900 mils -300 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -325 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 15) (pt 900 mils -400 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -425 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 16) (pt 900 mils -500 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -525 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 17) (pt 900 mils -600 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -625 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 18) (pt 900 mils -700 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -725 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 19) (pt 900 mils -800 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -825 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(pin (pinNum 20) (pt 900 mils -900 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 670 mils -925 mils) (rotation 0]) (justify "Right") (textStyleRef "Default"))
		))
		(line (pt 200 mils 100 mils) (pt 700 mils 100 mils) (width 6 mils))
		(line (pt 700 mils 100 mils) (pt 700 mils -1000 mils) (width 6 mils))
		(line (pt 700 mils -1000 mils) (pt 200 mils -1000 mils) (width 6 mils))
		(line (pt 200 mils -1000 mils) (pt 200 mils 100 mils) (width 6 mils))
		(attr "RefDes" "RefDes" (pt 750 mils 300 mils) (justify Left) (isVisible True) (textStyleRef "Default"))

	)
	(compDef "DS1013-20SSIB1-B-0" (originalName "DS1013-20SSIB1-B-0") (compHeader (numPins 20) (numParts 1) (refDesPrefix J)
		)
		(compPin "1" (pinName "1") (partNum 1) (symPinNum 1) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "3" (pinName "3") (partNum 1) (symPinNum 2) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "5" (pinName "5") (partNum 1) (symPinNum 3) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "7" (pinName "7") (partNum 1) (symPinNum 4) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "9" (pinName "9") (partNum 1) (symPinNum 5) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "11" (pinName "11") (partNum 1) (symPinNum 6) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "13" (pinName "13") (partNum 1) (symPinNum 7) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "15" (pinName "15") (partNum 1) (symPinNum 8) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "17" (pinName "17") (partNum 1) (symPinNum 9) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "19" (pinName "19") (partNum 1) (symPinNum 10) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "2" (pinName "2") (partNum 1) (symPinNum 11) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "4" (pinName "4") (partNum 1) (symPinNum 12) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "6" (pinName "6") (partNum 1) (symPinNum 13) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "8" (pinName "8") (partNum 1) (symPinNum 14) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "10" (pinName "10") (partNum 1) (symPinNum 15) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "12" (pinName "12") (partNum 1) (symPinNum 16) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "14" (pinName "14") (partNum 1) (symPinNum 17) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "16" (pinName "16") (partNum 1) (symPinNum 18) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "18" (pinName "18") (partNum 1) (symPinNum 19) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "20" (pinName "20") (partNum 1) (symPinNum 20) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(attachedSymbol (partNum 1) (altType Normal) (symbolName "DS1013-20SSIB1-B-0"))
		(attachedPattern (patternNum 1) (patternName "SHDR20W69P254X254_2X10_3300X91")
			(numPads 20)
			(padPinMap
				(padNum 1) (compPinRef "1")
				(padNum 2) (compPinRef "2")
				(padNum 3) (compPinRef "3")
				(padNum 4) (compPinRef "4")
				(padNum 5) (compPinRef "5")
				(padNum 6) (compPinRef "6")
				(padNum 7) (compPinRef "7")
				(padNum 8) (compPinRef "8")
				(padNum 9) (compPinRef "9")
				(padNum 10) (compPinRef "10")
				(padNum 11) (compPinRef "11")
				(padNum 12) (compPinRef "12")
				(padNum 13) (compPinRef "13")
				(padNum 14) (compPinRef "14")
				(padNum 15) (compPinRef "15")
				(padNum 16) (compPinRef "16")
				(padNum 17) (compPinRef "17")
				(padNum 18) (compPinRef "18")
				(padNum 19) (compPinRef "19")
				(padNum 20) (compPinRef "20")
			)
		)
		(attr "TME Electronic Components Part Number" "")
		(attr "TME Electronic Components Price/Stock" "")
		(attr "Manufacturer_Name" "Connfly")
		(attr "Manufacturer_Part_Number" "DS1013-20SSIB1-B-0")
		(attr "Description" "Socket; IDC; male; PIN: 20; straight; THT; gold-plated; 2.54mm")
		(attr "Datasheet Link" "https://www.tme.eu/Document/e9117e1c80532ff2c20cc520b4694ed9/DS1013.pdf")
		(attr "Height" "9.55 mm")
	)

)
