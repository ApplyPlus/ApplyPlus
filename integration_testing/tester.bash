
#Have this repo and the repo thats being patched in the same directory and run this bash script
touch result.txt
chmod +w result.txt
for path in ../patches/*; do
    git -C ./../../msm-3.10 reset --hard
    cd ./../../msm-3.10
    echo $path 
    echo $path >> ../vulnerableforks/integration_testing/result.txt
    echo "---------111--------------" >> ../vulnerableforks/integration_testing/result.txt
    python3 ../vulnerableforks/scripts/apply.py ../vulnerableforks/integration_testing/$path >> ../vulnerableforks/integration_testing/result.txt
    git diff >> ../vulnerableforks/integration_testing/result.txt
    echo "*****-------------------*-*-*------------------------" >> ../vulnerableforks/integration_testing/result.txt
    echo "------------------------*-*-*------------------------" >> ../vulnerableforks/integration_testing/result.txt
    cd ../vulnerableforks/integration_testing/
done
