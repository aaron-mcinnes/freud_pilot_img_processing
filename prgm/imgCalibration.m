%% converts images to hsv and cielab colour space and output stats
% uses SHINE_color https://github.com/RodDalBen/SHINE_color

%% Set base dirs
baseDir = fileparts(matlab.desktop.editor.getActiveFilename);
fprintf('%s\n',baseDir);

shineBase = fullfile(baseDir, 'SHINE_color', 'toolbox');
shineIn = fullfile(shineBase, 'SHINE_color_INPUT');
shineOut = fullfile(shineBase, 'SHINE_color_OUTPUT');

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
        targetDir = strrep(dirName, '2_croppedImg', '3_calibImg');
        targetPaths{end+1} = targetDir;
        if ~exist(targetDir, 'dir')
           mkdir(targetDir) 
        end
    end
end

%% calibrate images
%loop over source paths and copy to shine input folder (runs all images
%together)
for i = 1:size(sourcePaths,2)
    inputFolder = char(sourcePaths{i})
        %copy images to SHINE input folder
    copyfile(fullfile(inputFolder, '*'), shineIn);
    
end

%run SHINE on all images
cd(shineBase)
SHINE_color %requires user input.

%get the params used
contents = fullfile(shineOut, 'DIAGNOSTICS', 'params.txt');
params = readtable(contents);
colorspace = char(params.colorspace);
lumMode = char(params.luminanceMode);
specMode = char(params.spectralMode);
type = char(join({colorspace, lumMode, specMode}, '_'));

%copy all images to a single folder
outputFolder = fullfile(fileparts(targetDir), 'all', type);
if ~exist(outputFolder, 'dir')
    mkdir(outputFolder)
end
%extract output to target directory
movefile(fullfile(shineOut, '*'), outputFolder);
mkdir(fullfile(shineOut, 'DIAGNOSTICS')) ; %recreate the diagnostics folder in shine output directory
%clear the shine input
rmdir(shineIn, 's')
mkdir(shineIn)

%% Images to respective folders 
%separate images based on source dir
% Get a list of processed files
prefix =  ['SHINE_color_', colorspace, '*'];
fileList = dir(fullfile(outputFolder, prefix));
% Loop through each processed file
for i = 1:numel(fileList)
    % Get the source directory from the file name
    processedFileName = fileList(i).name;
    processedFilePath = fullfile(outputFolder, processedFileName);
    originalFileName = strrep(processedFileName, prefix(1:length(prefix)-1), '');
    
    for source = 1:numel(sourcePaths)
        fileChk = fullfile(sourcePaths{source}, originalFileName);
        if exist(fileChk, 'file') ~= 0
            targetDir = fullfile(targetPaths{source}, type);
            if ~exist(targetDir, 'dir')
                mkdir(targetDir)
            end
            targetPath = fullfile(targetDir, processedFileName);
            copyfile(processedFilePath, targetPath)
        end
    end
end

for source = 1:numel(sourcePaths)
    numSource = numel(dir(fullfile(sourcePaths{source}, '*.jpg')));
    numTarget = numel(dir(fullfile(targetPaths{source}, type, '*.jpg')));
    if numSource == numTarget
        disp(['Processed images copied to ', fullfile(targetPaths{source}, type)]);
    else
        disp(['ERROR in copying processed images to ', fullfile(targetPaths{source}, type)]);
    end
end
















