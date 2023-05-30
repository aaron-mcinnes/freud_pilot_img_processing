%% calculate and plot luminance/contrast of images

%%
clear 
close all
%% compare color matching methods

baseDir = fileparts(matlab.desktop.editor.getActiveFilename);
fprintf('%s\n',baseDir);

processedDir = fullfile(fileparts(baseDir), '3_calibImg', 'all');
dirs = dir(processedDir);
% Loop through the contents and identify folders
sourcePaths = cell(0);
targetPaths = cell(0);
stats = {};
numD = 0;
for i = 1:numel(dirs)
    if dirs(i).isdir && ~strcmp(dirs(i).name, '.') && ~strcmp(dirs(i).name, '..') 
        numD = numD + 1;
        dirName = dirs(i).name
        if strcmp(dirName, 'raw') %skip raw if it has been processed into the folder already
            continue
        end
        sourceDir = fullfile(processedDir, dirName);
        sourcePaths{end+1} = sourceDir;
        targetDir = fullfile(sourceDir, 'DIAGNOSTICS');
        targetPaths{end+1} = targetDir;
        paramsFile = fullfile(targetPaths{end}, 'params.txt');
        params = readtable(paramsFile);
        if strcmp(char(params.colorspace), 'cielab_')
            cs = 2;
        elseif strcmp(char(params.colorspace), 'hsv_')
            cs = 1;
        else
            cs = 0;
            disp('error detecting colorspace');
            break
        end
    
        [channel1, channel2, channel3, images, numim, imname] = readImages(sourceDir,'jpg',cs);
        stats{numD} = imstats(images);
        stats{numD}.type = dirName;
        title(dirName)
        label = ['M = ', num2str(stats{numD}.meanLum), ' ; SD = ', num2str(stats{numD}.meanStd)];
        xPos = 10;
        yPos = max(stats{numD}.meanHist);
        text(xPos, yPos, label, 'FontSize', 12, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'top');
        saveas(gcf, fullfile(targetDir, 'meanLumHist'));
        saveas(gcf, fullfile(targetDir, 'meanLumHist.png'));
        dirStats = stats{numD};
        save(fullfile(targetDir, 'lumStats'), 'dirStats');
        
        % extract image names to store with stats
        % Remove prefix
        shortNames = erase(imname, 'SHINE_color_cielab_');

        %save histMat (individual imgs) and meanHist (pooled) to .csv
        hists = [stats{numD}.histMat, stats{numD}.meanHist];
        histMat = array2table(hists);
        newNames = vertcat(shortNames, {'pooled'});
        histMat.Properties.VariableNames = newNames;
        writetable(histMat, fullfile(targetDir, 'histMat.csv'));
        
        %save meanVec and stdVec to .csv
        meanVec = num2cell(stats{numD}.meanVec);
        meanVec = [shortNames, num2cell(stats{numD}.meanVec), num2cell(stats{numD}.stdVec)];
        meanVec = cell2table(meanVec);
        meanVec.Properties.VariableNames = {'img', 'meanLum', 'sdLum'};
        writetable(meanVec, fullfile(targetDir, 'meanVec.csv'));
        
    end
end

%% same for raw images
sourceDir = fullfile(fileparts(baseDir), '2_croppedImg');
dirs = dir(sourceDir);
% Loop through the contents and identify folders
sourcePaths = cell(0);
targetPaths = cell(0);
for i = 1:numel(dirs)
    if dirs(i).isdir && ~strcmp(dirs(i).name, '.') && ~strcmp(dirs(i).name, '..') 
        dirName = dirs(i).name;
        dirName = fullfile(sourceDir, dirName);
        sourcePaths{end+1} = dirName;
    end
end

%loop over source paths and copy to shine input folder (runs all images
%together)
imagePaths = {};
for i = 1:size(sourcePaths,2)
    inputFolder = char(sourcePaths{i})
    fileList = dir(fullfile(inputFolder, '*.jpg')); 
    currentImagePaths = fullfile(inputFolder, {fileList.name});
    imagePaths = [imagePaths, currentImagePaths];
end

%copy to raw folder 
targetFolder = fullfile(processedDir, 'raw');
if ~exist(targetFolder, 'dir')
    mkdir(targetFolder)
end
for i = 1:numel(imagePaths)
    copyfile(imagePaths{i}, targetFolder); 
end

numD = numD + 1;
[channel1, channel2, channel3, images, numim, imname] = readImages(targetFolder,'jpg',2);
targetDir = fullfile(targetFolder, 'DIAGNOSTICS');
if ~exist(targetDir, 'dir')
    mkdir(targetDir)
end
stats{numD} = imstats(images);
stats{numD}.type = 'raw';
title('raw')
label = ['M = ', num2str(stats{numD}.meanLum), ' ; SD = ', num2str(stats{numD}.meanStd)];
xPos = 10;
yPos = max(stats{numD}.meanHist);
text(xPos, yPos, label, 'FontSize', 12, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'top');
saveas(gcf, fullfile(targetDir, 'meanLumHist'));
saveas(gcf, fullfile(targetDir, 'meanLumHist.png'));
dirStats = stats{numD};
save(fullfile(targetDir, 'lumStats'), 'dirStats');

% extract image names to store with stats
% Remove prefix
shortNames = erase(imname, 'SHINE_color_cielab_');

%save histMat (individual imgs) and meanHist (pooled) to .csv
hists = [stats{numD}.histMat, stats{numD}.meanHist];
histMat = array2table(hists);
newNames = vertcat(shortNames, {'pooled'});
histMat.Properties.VariableNames = newNames;
writetable(histMat, fullfile(targetDir, 'histMat.csv'));

%save meanVec and stdVec to .csv
meanVec = num2cell(stats{numD}.meanVec);
meanVec = [shortNames, num2cell(stats{numD}.meanVec), num2cell(stats{numD}.stdVec)];
meanVec = cell2table(meanVec);
meanVec.Properties.VariableNames = {'img', 'meanLum', 'sdLum'};
writetable(meanVec, fullfile(targetDir, 'meanVec.csv'));


%% compare minneapolis vs st paul
%cielab_histMatch2_sfMatch1 seems to give best balance of normalization
%with image clarity
close all 

match2use = 'cielab__histMatch2_sfMatch1'

%load images from each dir
sourceDir = fullfile(fileparts(baseDir), '3_calibImg');
dirs = dir(sourceDir);
% Loop through the contents and identify folders
sourcePaths = cell(0);
targetPaths = cell(0);
for i = 1:numel(dirs)
    if dirs(i).isdir && ~strcmp(dirs(i).name, '.') && ~strcmp(dirs(i).name, '..') 
        dirName = dirs(i).name;
        dirName = fullfile(sourceDir, dirName);
        if strcmp(dirs(i).name, 'all') 
            continue
        else
            sourcePaths{end+1} = dirName;
        end
    end    
end

stats = {};
%loop over selected image folders 
for path = 1:numel(sourcePaths)
    %get image statistics in folder
    paramsPath = fullfile(sourceDir, 'all', match2use, 'DIAGNOSTICS', 'params.txt');
    params = readtable(paramsPath);
    %get colorspace
    if strcmp(char(params.colorspace), 'cielab_')
        cs = 2;
    elseif strcmp(char(params.colorspace), 'hsv_')
        cs = 1;
    else
        cs = 0;
        disp('error detecting colorspace');
        break
    end
    
    %read images
    imgPath = fullfile(sourcePaths{path}, match2use);
    targetDir = fullfile(imgPath, 'DIAGNOSTICS');
    if ~exist(targetDir)
        mkdir(targetDir)
    end
    [channel1, channel2, channel3, images, numim, imname] = readImages(imgPath,'jpg',cs);
    stats{path} = imstats(images);
    [~, folderName, ~] = fileparts(sourcePaths{path});
    stats{path}.type = folderName;
    if strcmp(folderName, 'msp') %clearer title just for plot
        imgTitle = 'Minneapolis';
    elseif strcmp(folderName, 'stp')
        imgTitle = 'StPaul';
    end
    title(imgTitle)
    label = ['M = ', num2str(stats{path}.meanLum), ' ; SD = ', num2str(stats{path}.meanStd)];
    xPos = 10;
    yPos = max(stats{path}.meanHist);
    text(xPos, yPos, label, 'FontSize', 12, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'top');
    saveas(gcf, fullfile(targetDir, 'meanLumHist'));
    saveas(gcf, fullfile(targetDir, 'meanLumHist.png'));
    dirStats = stats{path};
    save(fullfile(targetDir, 'lumStats'), 'dirStats');
    
end



