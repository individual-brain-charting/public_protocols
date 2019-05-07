%% This script resizes the input images of the stimuli
%%
%% Author: Ana Luísa Pinho
%% e-mails: ana.pinho@inria.fr
%%
%% =======================================================

%% Load image package
pkg load image

%% Number of inputs
total_items = 4;

inputs_folder = 'rewardim';
group_category = 'training_food';
category = 'example';
filetype = '.bmp';

%% Output directory
newSubFolder = [inputs_folder, filesep, group_category, '_resized'];

resize_factor = 1.5

%% Create output folder if does not exist
if ~exist(newSubFolder, 'dir')
  mkdir(newSubFolder);
end

%% Load images, resize them and save them in the output folder
for iItem = 1:total_items
  image_input = imread([inputs_folder, filesep, group_category, filesep, category, '_', num2str(iItem), filetype]);
  image_input_resized = imresize(image_input, resize_factor);
  imwrite (image_input_resized, [newSubFolder, filesep, category, '_', num2str(iItem), filetype]);
end
