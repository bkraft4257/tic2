

# Apply Transform
https://mail.nmr.mgh.harvard.edu/pipermail//freesurfer/2017-October/054453.html

glad to hear it worked! You can control the conversion to int by using

 	-odt, --out_data_type <uchar|short|int|float>

cheers
Bruce


On Sun, 22 Oct 2017, Gidon Levakov wrote:

> Hi,
>
> I think I got the problem, just updating, so other people won't do the same mistake:
>
> The warp stored in the 'talairach.m3z' file should be applied on a conformed volume, meaning the raw
> image after the the following command was cried out:
> "mri_convert img.nii.gz img_conformed.nii.gz --conform" (conform to 1mm voxel size in coronal)
>
> then the warp can simply applied by the following command:
> 'mri_convert img_conformed.nii.gz --apply_transform talairach.m3z -oc 0 0 0 img_warped.nii' (works
> for me!)
>
> I also noticed that the '--conform' option convert the img data type to integer (if it was float
> before, like in my case, where it turned all the values to 0). So you should be aware to that.
>
> Good luck!
> gidon l.
>
>
> 2017-10-19 16:40 GMT+03:00 Gidon Levakov <gidonle at post.bgu.ac.il>:
>       Hi Freesurfer experts,
>
> I have several nifti images (created with another software) in the subjects original
> anatomical space (native space) that I want to transform to a common space (freesurfer version
> of MNI305 should be fine) using non-linear transformation.
>
> Reading a previous answer regarding this issue
> (https://mail.nmr.mgh.harvard.edu/pipermail//freesurfer/2013-September/033556.html), I
> understand I should use the mri_vol2vol command to apply the transformation stored in the file
> mri/transforms/talairach.m3z (I already run recon all). But after checking the result, the
> images are still not align with each other and do not resemble the mni305.cor.mgz file.
>
> I used the following command:
>
> mri_vol2vol --m3z my_subjects_dir/sub_X/mri/transforms/talairach.m3z --noDefM3zPath
> --reg_header --mov file_loc/img.nii.gz --targ /usr/local/freesurfer/average/mni305.cor.mgz --o
> file_loc/img_warped.nii.gz
>
> I also tried without the --reg_header option with no success.
>
> Any idea what I am doing wrong? can you give me an example that works?
>
> Thanks in advance!
>
> Gidon l.
>
>