package com.monsterxia.simpletry.texttorandom;

import java.io.*;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * The Class is used to shuffle the target layer rotation pool.
 * Rules:
 * 1. Randomize.
 * 2. Space at least N layers between the same levels.
 * @author monsterXia
 * @version 1.0.1
 * @date Jan.21st.2023
 */
public class RandomRank {
    /**
     * Set the minimum number of layers between the same levels, changeable.
     */
    public static final int INTERVALS_AT_LEAST_BETWEEN_SAME_LEVEL = 11;

    public static void main(String[] args) {
        //Address of source LayerRotation.cfg.
        String fileAddress = "src/com/monsterxia/simpletry/texttorandom/LayerRotation.cfg";
        //Address of target LayerRotation.cfg. You do can just cover the original one.
        String targetFileAddress = "src/com/monsterxia/simpletry/texttorandom/TargetLayerRotation.cfg";

        shuffle(fileAddress,targetFileAddress);
    }

    /**
     * get Total line in original LayerRotation.cfg.
     * @param fileAddress Source LayerRotation.cfg
     * @return Total line in LayerRotation.cfg
     */
    private static int getSumOfLines(String fileAddress){
        int sum = 0;
        try{
            BufferedReader reader = new BufferedReader(new FileReader(fileAddress));
            String line = reader.readLine();
            while(line != null){
                sum += 1;
                line= reader.readLine();
            }

            reader.close();
        }catch (IOException e){
            e.printStackTrace();
        }
        return sum;
    }

    /**
     * Generate a random index array of specified length.
     * @param targetLength Total length of random array to be generated
     * @return Random index array of specified length
     */
    private static int[] getRandomIndexArray(int targetLength){
        Integer[] index = new Integer[targetLength];
        int[] randomIndex = new int[targetLength];
        for (int i = 0; i < targetLength; i++) {
            index[i] = i;
        }
        List<Integer> list = Arrays.asList(index);
        Collections.shuffle(list);
        index = list.toArray(new Integer[0]);

        for (int i = 0; i < targetLength; i++) {
            randomIndex[i] = index[i];
        }

        return randomIndex;
    }

    /**
     * Convert the layer data in the original LayerRotation.cfg into a layer array.
     * @param fileAddress Source LayerRotation.cfg
     * @return Layer array
     */
    private static Layer[] getLayerFromFile(String fileAddress){
        int totalLayer = getSumOfLines(fileAddress);
        Layer[] layerArray = new Layer[totalLayer];
        try{
            BufferedReader reader = new BufferedReader(new FileReader(fileAddress));
            for (int i = 0; i < totalLayer; i++) {
                String line = reader.readLine();
                layerArray[i] = new Layer(line);
            }
            reader.close();
        }catch (IOException e){
            e.printStackTrace();
        }
        return layerArray;
    }

    /**
     * Scramble the original layer array to get a random array.
     * @param sourceLayerArray Original layer array
     * @return Random layer array
     */
    private static Layer[] randomRank(Layer[] sourceLayerArray){
        Layer[] resultLayerArray = new Layer[sourceLayerArray.length];
        int[] randomIndexArray = getRandomIndexArray(sourceLayerArray.length);
        for (int i = 0; i < sourceLayerArray.length; i++) {
            resultLayerArray[randomIndexArray[i]]= sourceLayerArray[i];
        }
        return resultLayerArray;
    }

    /**
     * Adjust the order of elements in the original array.
     * So that at least N elements of other levels are separated between two elements of the same level.
     * @param preliminaryLayerRotation Array to be processed
     * @return Arrays processed according to rules
     */
    public static synchronized Layer[] sameLevelFix(Layer[] preliminaryLayerRotation) {
        Layer[] resultLayerArray = new Layer[preliminaryLayerRotation.length];
        resultLayerArray[0] = preliminaryLayerRotation[0];

        for (int j = 1; j < preliminaryLayerRotation.length; j+=1) {
            boolean replaceFlag = false;
            for(int k = 1; j-k >= 0 && k<=INTERVALS_AT_LEAST_BETWEEN_SAME_LEVEL; k++){
                if( preliminaryLayerRotation[j].getLevel().equals( preliminaryLayerRotation[j-k].getLevel() ) ){
                    for (int l = j+1; l < preliminaryLayerRotation.length; l++) {
                        boolean replaceable = true;
                        for (int m = 1; m <= INTERVALS_AT_LEAST_BETWEEN_SAME_LEVEL && j-m >=0; m++) {
                            if(preliminaryLayerRotation[j-m].getLevel().equals(preliminaryLayerRotation[l].getLevel())){
                                replaceable = false;
                                break;
                            }
                        }

                        if (replaceable){
                            replaceFlag = true;
                            resultLayerArray[j]=preliminaryLayerRotation[l];

                            preliminaryLayerRotation[l] = preliminaryLayerRotation[j];
                            preliminaryLayerRotation[j] = resultLayerArray[j];
                            break;
                        }
                    }
                }
                if (replaceFlag){
                    break;
                }
            }
            if (!replaceFlag){
                resultLayerArray[j]=preliminaryLayerRotation[j];
            }
        }

        return resultLayerArray;
    }

    /**
     * Write the processed Layer array into a file for storage.
     * @param targetFileAddress Location to save
     * @param finalLayerArray Layer array processed
     */
    private static void setLayerToFile(String targetFileAddress,Layer[] finalLayerArray){
        try{
            BufferedWriter writer = new BufferedWriter(new FileWriter(targetFileAddress));

            for (Layer tempLayer: finalLayerArray) {
                writer.write(tempLayer.getLayerName());
                writer.newLine();
            }
            writer.close();
        }catch (IOException e){
            e.printStackTrace();
        }
    }

    /**
     * 1.Read the data from the specified target.
     * 2.Save it to the specified location after scrambling based on certain rules.
     * Process integration.
     * @param fileAddress Source LayerRotation.cfg
     * @param targetFileAddress Target LayerRotation.cfg
     */
    private static void shuffle(String fileAddress,String targetFileAddress){
        Layer[] originalLayerRotation = getLayerFromFile(fileAddress);
        Layer[] preliminaryLayerRotation = randomRank(originalLayerRotation);
        Layer[] targetLayerRotation = sameLevelFix(preliminaryLayerRotation);
        setLayerToFile(targetFileAddress,targetLayerRotation);
    }
}

/**
 * Layer class, used to generate a class with corresponding member variable based on layer's name.
 * layerName,level,mode already have been done
 */
class Layer {
    /**
     * Defines an immediate constant, which is used to compare and identify annotation symbols.
     */
    static final char ANNOTATION_SIGNAL = '/';
    /**
     * Defines an immediate constant, which is used to compare and identify underscore symbols.
     */
    static final char UNDERLINE_SIGNAL = '_';
    /**
     * The annotation is represented by 2 consecutive slashes.
     * Defining the immediate number used to remove the annotation symbol.
     */
    static final int ANNOTATION_FIX = 2;

    /**
     * layer' Name.
     */
    private final String layerName;
    /**
     * Layer's Level.
     */
    private String level;
    /**
     * Layer's mode.
     */
    private String mode;

    /**
     * Use layer' Name to get other member variable.
     */
    private void memberPropertyUpdate(){
        char[] letterArray = this.layerName.toCharArray();

        if( letterArray[0] == ANNOTATION_SIGNAL && letterArray[1] == ANNOTATION_SIGNAL){
            System.arraycopy(letterArray, 2, letterArray, 0, letterArray.length - ANNOTATION_FIX);
        }

        int firstUnderlineIndex = 0;
        for (int i = 0; i < letterArray.length; i++) {
            if ( letterArray[i] == UNDERLINE_SIGNAL){
                firstUnderlineIndex = i;
                break;
            }
        }

        assert firstUnderlineIndex != 0;
        this.level = new String(letterArray, 0, firstUnderlineIndex);

        int secondUnderlineIndex = 0;
        for (int i = firstUnderlineIndex+1; i < letterArray.length; i++) {
            if ( letterArray[i] == UNDERLINE_SIGNAL){
                secondUnderlineIndex = i;
                break;
            }
        }

        if (secondUnderlineIndex == 0){
            this.mode = "Training";
        }else{
            this.mode = new String(letterArray, firstUnderlineIndex+1, secondUnderlineIndex - firstUnderlineIndex -1);
        }
    }

    /**
     * Get layer' Name.
     * @return layer' Name
     */
    public String getLayerName() {
        return this.layerName;
    }

    /**
     * Get layer' Level.
     * @return layer' Level
     */
    public String getLevel() {
        return this.level;
    }

    /**
     * Get layer' Mode.
     * @return layer' Mode
     */
    public String getMode() {
        return this.mode;
    }

    /**
     * Use layer' Name to generate layer object.
     * @param stringOfLayerName Main variable to generate other variables
     */
    public Layer(String stringOfLayerName){
        this.layerName = stringOfLayerName;
        this.memberPropertyUpdate();
    }
}
